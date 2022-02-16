### Training & Evaluation

Detectron2 is used as the framework for training & evaluation and the Faster RCNN network. We will be using
yaml configs for these operations. There are a few samples in the `config/` folder.


#### Training steps

##### Step 0: Initialization

Please follow `docs/setup-training-environment.md#directory-structure` and make sure
the datasets are in the expected folders.

When using synthetic data we use transfer learning and initialize the
network with [Imagenet-R-50.pkl](https://dl.fbaipublicfiles.com/detectron/ImageNetPretrained/MSRA/R-50.pkl) weights.
We also try without using transfer learning for this step, by turning `config.train.transfer_learning.enabled` to `False`.

##### Step 1: Pre-training with synthetic data:

Based on the amount of synthetic data used we will setup the no. of iterations in the config.

For e.g.

```
size of dataset: 10k
batch size: 16
no. of iterations: 10000/16 = 625
total iterations: 170000
no. of epochs: 272
```

So for this example we will update `config/detectron_dog_detection.yml` with the following:

```
model:
  workers: 1
  gpu: 0
  IMS_PER_BATCH: 16 <-- (batch size)
  base_lr: 0.00025
  MAX_ITER: 170000 <-- (iterations)
  resume: True
  REFERENCE_WORLD_SIZE: 1
  FREEZE_AT: 0
  BATCH_SIZE_PER_IMAGE: 128
  NUM_CLASSES: 1
  CHECKPOINT_PERIOD: 10000
  STEPS: (110000, 150000)
  EVAL_PERIOD: 5000
  TTA_ENABLED: False
  config_yaml: faster_rcnn_R_50_FPN_3x.yaml
```

To start training:

- `cd` into the project.
- Run -
```shell
python -m src.run train -c config/detectron_dog_detection.yml --train_data=data --val_data=data --checkpoint-dir=ckpt
```




This will start the training. The `config/detectron_dog_detection.yml` is configured to run on CPU. If you want to
run on GPUs, please use `config/detectron_dog_detection.yml` and update the `model.gpus` to the number
of GPUs available. Currently it's configured to 8, which is what we used for running our experiments.

After the training is complete it will write the models into a folder with a timestamp. That
will be printed in the log.

##### Step 2: Fine tune with real data:

For fine-tuning with the 1200 real images, which is expected at `data/real/<split>/coco_train2017.json`.
This would provide all metadata required to refer to the 1200 real images which will be used to finetune.

Here's a [link]() to download it. Before we start the fine-tuning training, please update the config block
as follows:

```
size of dataset: 1200
batch size: 16
no. of iterations: 1200/16 = 75
total iterations: 27000
no. of epochs: 360
```

```
train:
  dataset:
    name: indoor_dog
    data_split: train
    synth: False
  transfer_learning:
    enabled: True
    checkpoint: <folder-name>

model:
  workers: 1
  gpu: 0
  IMS_PER_BATCH: 16 <-- (batch size)
  base_lr: 0.00025
  MAX_ITER: 27000 <-- (iterations)
  resume: True
  REFERENCE_WORLD_SIZE: 1
  FREEZE_AT: 0
  BATCH_SIZE_PER_IMAGE: 128
  NUM_CLASSES: 1
  CHECKPOINT_PERIOD: 10000
  STEPS: (21000, 25000)
  EVAL_PERIOD: 1000
  TTA_ENABLED: False
  config_yaml: faster_rcnn_R_50_FPN_3x.yaml
```

`<folder-name>` refers to the output folder name from Step 1.

And restart the training with:

```shell
python -m src.run train -c config/detectron_dog_detection.yml --train_data=data --val_data=data --checkpoint-dir=ckpt
```

This will generate a checkpoint which is trained on synthetic & fine-tuned on the 1200 real world data.



##### Step 3: Evaluate on real data:

We will be using detectron2 yaml configs for training our model. We will be using 2 methodologies -

* Initializing from Imagenet-R-50.pkl checkpoint.
* Not starting from a checkpoint.

For running the training please follow the instructions below:

1. `cd` into the project directory i.e. `demos/dog_detection/`
3. `python __main__.py train -c config/detectron_dog_detection.yaml --train-data=<train-data-path> --val-data=<val-data-path>data --checkpoint-dir=<output-dif>`
4. For testing - `python  __main__.py evaluate -c config/detectron_dog_detection.yaml --test-data=<test-data-path> --checkpoint-file=<checkpoint-file>`
