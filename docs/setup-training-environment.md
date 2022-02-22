### Setup Environment

### Pre requisites
* conda (Please follow [Link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) for installing conda)
* cuda drivers (If GPU available)

#### Setup Conda


1. `conda create --file environment.yml -n unity-cv-dog-detection python=3.8`
2. `conda activate unity-cv-dog-detection`
3. `conda env update -n unity-cv-dog-detection --file environment.yml`


N.B. - We use 8 Nvidia V100 GPUs for our experiments.

## Datasets

We trained with multiple strategies using real & synthetic data. The following explains the datasets we used:

### Real data

We used real data for fine-tuning & testing the final models for performance.
[COCO](https://cocodataset.org/#home) and [OIDSv6](https://storage.googleapis.com/openimages/web/index.html) was
filtered with classes including `dog` and indoor artifacts like `microwave`, `couch` etc.

This resulted in a total of 1538 images, and we split it -

| Task        | No. of images (real) |
|-------------|----------------------|
| fine-tuning | 1200                 |
| validation  | 138                  |
| test        | 200                  |


TODO: Update links to datasets (@souranil)

Download the datasets from [here]()


### Synthetic

We use the "Home Interior" template, and use the "dogs asset pack", for generating
different amounts of synthetic data while keeping the data distribution similar to
the real data.

The no. of frames we experimented with are:

- 5k
- 10k
- 40k
- 100k


### Directory Structure

Make sure you download the datasets to the following folder structure:

```
project
└───data
│   └───synth
│   │     └───train-10k
│   │         └───annotations
│   │         │      coco_object_detection_annotations.json <-- (synthetic train)
│   │         └───images
│   └───real
│         └───train2017
│         │   └───annotation
│         |   │     coco.json
│         |   └───images
│         └───val2017
│             └───annotation
│             │     coco.json
│             └───images
```
