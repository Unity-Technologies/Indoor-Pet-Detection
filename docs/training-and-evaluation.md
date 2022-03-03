### Training & Evaluation

Detectron2 is used as the framework for training & evaluation and the Faster RCNN network. We will be using YAML configs for these operations. There are a few samples in the `config/` folder.

We will be using detectron2 YAML configs for training our model. We will be using 2 methodologies -

* Initializing from Imagenet-R-50.pkl checkpoint.
* Not starting from a checkpoint.

#### Training steps

##### Step 0: Initialization

Please follow the [**Prerequisites**](prerequisites.md#setup-training-environment) to set up the Python environment and datasets for the model training. Make sure the datasets are in the expected folders.

##### Step 1: Pre-training with synthetic data:

When using synthetic data we use transfer learning and initialize the network with [Imagenet-R-50.pkl](https://dl.fbaipublicfiles.com/detectron/ImageNetPretrained/MSRA/R-50.pkl) weights. We also try without using transfer learning for this step, by turning `config.train.transfer_learning.enabled` to `False`.

Based on the amount of synthetic data used we will set up the no. of iterations in the config.

For example,

```
size of dataset: 10k
batch size: 16
no. of iterations: 10000/16 = 625
total iterations: 170000
no. of epochs: 272
```

So for this example, we will update the `train` and `model` configurations in the `config/detectron_dog_detection.yml` with the following:

```
train:
  dataset:
    name: indoor_pet_detection
    synth: True
  transfer_learning:
    enabled: False
    checkpoint: COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml

...

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
python -m src.run train -c config/detectron_dog_detection.yaml --train-data=data/synth/train-10k --val-data=data/real/val2017
```

This will start the training. The `config/detectron_dog_detection.yaml` is configured to run on CPU. If you want to run on GPUs, please use `config/detectron_dog_detection_gpu.yaml` and update the `train` and `model` configurations as above. The `model.gpus` should be updated to the number of GPUs available on your platform. Currently it's configured to 8, which is what we used for running our experiments.

After the training is complete it will write the models into the `output/` folder with a timestamp. That
will be printed in the log.

Use Tensorboard to view the training progress

1. Open terminal and run `tensorboard --logdir=output`

2. In your favorite browser, start Tensorboard `http://localhost:6006/`

##### Step 2: Fine tune with real data:

For fine-tuning with the 1200 real images, which is expected at `data/real/train2017/annotations/coco.json`.
This would provide all metadata required to refer to the 1200 real images which will be used to finetune.

Here's a [link](https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1/real_datasets.zip) to download it. Before we start the fine-tuning training, please update the config block
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
    checkpoint: <folder-name>/model_final.pth

...

model:
  workers: 1
  gpu: 0
  IMS_PER_BATCH: 16 <-- (batch size)
  base_lr: 0.00025
  MAX_ITER: 27000 <-- (iterations)
  resume: False    <-- (don't resume iterations)
  REFERENCE_WORLD_SIZE: 1
  FREEZE_AT: 0
  BATCH_SIZE_PER_IMAGE: 128
  NUM_CLASSES: 1
  CHECKPOINT_PERIOD: 10000
  STEPS: (21000, 25000) <-- (steps)
  EVAL_PERIOD: 1000 <-- (evaluation period)
  TTA_ENABLED: False
  config_yaml: faster_rcnn_R_50_FPN_3x.yaml
```

`<folder-name>` refers to the output folder name from Step 1.

And restart the training with:

```shell
python -m src.run train -c config/detectron_dog_detection.yaml --train-data=data/real/train2017 --val-data=data/real/val2017
```

This will generate a checkpoint into the `output/` folder with a timestamp, which is trained on synthetic & fine-tuned on the 1200 real world data.

##### Step 3: Evaluate on real data:

Update the config test block as the following, and replace the `<timestamp>` to your output folder from Step 2.

```
test:
  dataset:
    name: real_images
    synth: False
  checkpoint: <folder-name>/model_final.pth
```

`<folder-name>` refers to the output folder name from Step 2.

Use the following command line to trigger the evaluation.

```shell
python -m src.run evaluate -c config/detectron_dog_detection.yaml --test-data=data/real/test2017
```

#### Trouble Shooting

##### Incompatible library version: \_imaging.cpython-39-darwin.so requires version 14.0.0 or later

Try `conda install -c conda-forge dlib` to fix the issue [[Reference]](https://github.com/python-pillow/Pillow/issues/5257)

---

#### Proceed to [Results](results.md)
