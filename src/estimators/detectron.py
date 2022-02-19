# Copyright (c) Unity Technologies USA Inc.
import glob
import logging
import os
from collections import OrderedDict
from datetime import datetime

import detectron2.utils.comm as comm
import torch
from detectron2 import model_zoo
from detectron2.checkpoint import DetectionCheckpointer, PeriodicCheckpointer
from detectron2.config import get_cfg
from detectron2.data import (MetadataCatalog, build_detection_test_loader,
                             build_detection_train_loader)
from detectron2.data.datasets import register_coco_instances
from detectron2.engine import (default_argument_parser, default_setup,
                               default_writers, launch)
from detectron2.evaluation import (COCOEvaluator, DatasetEvaluators,
                                   inference_on_dataset, print_csv_format)
from detectron2.modeling import build_model
from detectron2.solver import build_lr_scheduler, build_optimizer
from detectron2.utils.events import EventStorage
from detectron2.utils.logger import setup_logger
from torch.nn.parallel import DistributedDataParallel

import src.constants as const

TIMESTAMP_SUFFIX = datetime.now().strftime("%Y%m%d-%H%M%S")


setup_logger()
logger = logging.getLogger(__name__)
logger.info(f"{torch.__version__}, {torch.cuda.is_available()}")


class DetectronEstimator:
    def __init__(
        self, *, config, checkpoint_dir=None, train_data=None, test_data=None, **kwargs
    ):
        self.config = config
        logger.info(f"initializing detectron estimator")
        self.checkpoint_dir = checkpoint_dir
        self.train_data = train_data
        self.test_data = test_data

        if torch.cuda.is_available():
            n = torch.cuda.device_count()
            logger.info(f"No of cuda device: {n}")  # emoji-safe
            s = " "
            for i, d in enumerate(range(n)):
                p = torch.cuda.get_device_properties(i)
                s += f" CUDA:{d} ({p.name}, {p.total_memory / 1024 ** 2}MB)\n"  # bytes to MB
            logger.info(s.encode().decode("ascii", "ignore"))  # emoji-safe

    def main(self, args, test_data, train_data):
        cfg = setup(args)
        if test_data:
            cfg.DATASETS.TEST = ("synth_coco_val",)
            is_synth = self.config.test.dataset.synth
            annotation_path, images_path = get_dataset_metadata(
                self.test_data, is_synth=is_synth
            )
            register_coco_instances("synth_coco_val", {}, annotation_path, images_path)

        if train_data:
            cfg.DATASETS.TRAIN = ("synth_coco_train",)
            is_synth = self.config.train.dataset.synth
            annotation_path, images_path = get_dataset_metadata(
                self.train_data, is_synth=is_synth
            )
            register_coco_instances(
                "synth_coco_train", {}, annotation_path, images_path
            )

        for d in ["train", "val"]:
            MetadataCatalog.get("synth_coco_" + d).thing_classes = const.CLASSES

        model = build_model(cfg)
        if args.eval_only:
            DetectionCheckpointer(model, save_dir=cfg.OUTPUT_DIR).resume_or_load(
                cfg.MODEL.WEIGHTS, resume=args.resume
            )
            return self.do_eval(cfg, model)
        distributed = comm.get_world_size() > 1
        if distributed:
            model = DistributedDataParallel(
                model, device_ids=[comm.get_local_rank()], broadcast_buffers=True
            )
        self.do_train(cfg, model, resume=args.resume)
        return self.do_eval(cfg, model)

    def run(self, eval_only=False):
        args = default_argument_parser().parse_args()
        args.resume = self.config.model.resume
        args.num_gpus = self.config.model.gpu
        args.config_file = "config/detectron/" + self.config.model.config_yaml
        args.eval_only = eval_only
        args.resume = self.config.model.resume
        arguments = args_fine_tune(self.config)
        logger.info(f"args_transfer_learning prepared: {arguments}")
        args.opts = arguments
        logger.info(f"\n\n[*] Training Args: {args}\n\n")

        launch(
            self.main,
            self.config.model.gpu,
            num_machines=args.num_machines,
            machine_rank=args.machine_rank,
            dist_url=args.dist_url,
            args=(args, self.test_data, self.train_data),
        )

    def _set_checkpoint(self, checkpoint):
        """
        Returns a path or URI to a checkpoint
        Args:
            checkpoint: Path or URI to checkpoint.

        Returns:
            Path to checkpoint
        """
        if "COCO-Detection" in checkpoint:
            return model_zoo.get_checkpoint_url(checkpoint)
        elif ".pth" in checkpoint:
            return checkpoint
        elif "detectron2://" in checkpoint:
            return checkpoint
        return checkpoint

    def get_evaluator(self, cfg, dataset_name, output_folder=None):
        """
        Create evaluator(s) for a given dataset.
        This uses the special metadata "evaluator_type" associated with each builtin dataset.
        For your own dataset, you can simply create an evaluator manually in your
        script and do not have to worry about the hacky if-else logic here.
        """
        if output_folder is None:
            output_folder = os.path.join(cfg.OUTPUT_DIR, "inference")
        evaluator_list = []
        MetadataCatalog.list()
        evaluator_type = MetadataCatalog.get(dataset_name).evaluator_type
        logger.debug(f"Evaluator type: {evaluator_type}")
        if evaluator_type in ["coco"]:
            evaluator_list.append(COCOEvaluator(dataset_name, cfg, True, output_folder))

        if len(evaluator_list) == 0:
            raise NotImplementedError(
                "no Evaluator for the dataset {} with the type {}".format(
                    dataset_name, evaluator_type
                )
            )
        elif len(evaluator_list) == 1:
            return evaluator_list[0]
        return DatasetEvaluators(evaluator_list)

    def do_eval(self, cfg, model):
        results = OrderedDict()
        for dataset_name in cfg.DATASETS.TEST:
            data_loader = build_detection_test_loader(cfg, dataset_name)
            evaluator = self.get_evaluator(
                cfg,
                dataset_name,
                os.path.join(cfg.OUTPUT_DIR, "inference", dataset_name),
            )
            results_i = inference_on_dataset(model, data_loader, evaluator)
            results[dataset_name] = results_i
            if comm.is_main_process():
                logger.info(
                    "Evaluation results for {} in csv format:".format(dataset_name)
                )
                print_csv_format(results_i)
        if len(results) == 1:
            results = list(results.values())[0]
        return results

    def do_train(self, cfg, model, resume=False):
        model.train()
        optimizer = build_optimizer(cfg, model)
        scheduler = build_lr_scheduler(cfg, optimizer)

        checkpointer = DetectionCheckpointer(
            model, cfg.OUTPUT_DIR, optimizer=optimizer, scheduler=scheduler
        )

        transfer_learning_enabled = self.config.train.transfer_learning.enabled
        if transfer_learning_enabled and resume:
            # The checkpoint stores the training iteration that just finished, thus we start
            # at the next iteration
            cfg.MODEL.WEIGHTS = self._set_checkpoint(
                self.config.train.transfer_learning.checkpoint
            )
            start_iter = (
                checkpointer.resume_or_load(cfg.MODEL.WEIGHTS, resume=resume).get(
                    "iteration", -1
                )
                + 1
            )
        else:
            start_iter = 0

        max_iter = cfg.SOLVER.MAX_ITER

        periodic_checkpointer = PeriodicCheckpointer(
            checkpointer, cfg.SOLVER.CHECKPOINT_PERIOD, max_iter=max_iter
        )

        writers = (
            default_writers(cfg.OUTPUT_DIR, max_iter) if comm.is_main_process() else []
        )
        logger.info("Starting training from iteration {}".format(start_iter))
        data_loader = build_detection_train_loader(cfg)

        with EventStorage(start_iter) as storage:
            for data, iteration in zip(data_loader, range(start_iter, max_iter)):
                storage.iter = iteration
                logger.debug(f"Training Iter: {iteration}")
                loss_dict = model(data)
                losses = sum(loss_dict.values())
                assert torch.isfinite(losses).all(), loss_dict

                loss_dict_reduced = {
                    k: v.item() for k, v in comm.reduce_dict(loss_dict).items()
                }
                losses_reduced = sum(loss for loss in loss_dict_reduced.values())
                if comm.is_main_process():
                    storage.put_scalars(total_loss=losses_reduced, **loss_dict_reduced)

                optimizer.zero_grad()
                losses.backward()
                optimizer.step()
                storage.put_scalar(
                    "lr", optimizer.param_groups[0]["lr"], smoothing_hint=False
                )
                scheduler.step()

                if (
                    cfg.TEST.EVAL_PERIOD > 0
                    and (iteration + 1) % cfg.TEST.EVAL_PERIOD == 0
                    and iteration != max_iter - 1
                ):
                    self.do_eval(cfg, model)
                    comm.synchronize()

                if iteration - start_iter > 5 and (
                    (iteration + 1) % 20 == 0 or iteration == max_iter - 1
                ):
                    for writer in writers:
                        writer.write()
                periodic_checkpointer.step(iteration)


def get_dataset_metadata(data_path):
    annotation_match = glob.glob(f"{data_path}/annotations*/*.json")
    if len(annotation_match) == 0 or len(annotation_match) > 1:
        raise Exception(f"Valid annotation not found at {data_path}")
    annotation_path = annotation_match[0]
    images_path = f"{data_path}/images"

    return (
        annotation_path,
        images_path
    )


def args_fine_tune(config):
    return [
        "DATALOADER.NUM_WORKERS",
        config.model.workers,
        "TEST.EVAL_PERIOD",
        config.model.EVAL_PERIOD,
        "SOLVER.IMS_PER_BATCH",
        config.model.IMS_PER_BATCH,
        "SOLVER.BASE_LR",
        config.model.base_lr,
        "MODEL.BACKBONE.FREEZE_AT",
        "0",
        "SOLVER.GAMMA",
        "0.1",
        "SOLVER.STEPS",
        config.model.STEPS,
        "SOLVER.MAX_ITER",
        config.model.MAX_ITER,
        "SOLVER.CHECKPOINT_PERIOD",
        config.model.CHECKPOINT_PERIOD,
        "SOLVER.REFERENCE_WORLD_SIZE",
        config.model.REFERENCE_WORLD_SIZE,
        "MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE",
        config.model.BATCH_SIZE_PER_IMAGE,
        "MODEL.ROI_HEADS.NUM_CLASSES",
        config.model.NUM_CLASSES,
    ]


def setup(args):
    """
    Create configs and perform basic setups.
    """
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda"
    cfg.MODEL.DEVICE = device
    default_setup(cfg, args)
    return cfg
