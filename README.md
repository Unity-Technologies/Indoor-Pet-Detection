# Indoor Pet Detection Example


[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE.md)
![Unity](https://img.shields.io/badge/unity-2020.3.21f-brightgreen)

This project provides scripts necessary to train a model for dog detection in an
indoor home environment, with Unity generated Synthetic Data, and evaluate your model. For this example,
we will use synthetic data to train our model and real data from COCO and OIDSv6 to
fine tune and test our model.

We also show how we can upload our own custom assets, and change randomizer parameters
to change the data as required. Unity Computer Vision Datasets (UCVD) is the cloud platform
used for generating large scale datasets.

### Instructions

1. [Prerequisites](docs/prerequisites.md)
2. [Create a synthetic dataset for dog detection with UCVD](docs/dataset-generation-and-configuration.md)
3. [Training, Fine-tuning & Evaluation](docs/training-and-evaluation.md)
4. [Results](docs/results.md)

[//]: # (N.B. - We have used Detectron2 for this project, and to know more about it, please chckout - [Detectron2]&#40;https://github.com/facebookresearch/detectron2&#41;.)

### Learning More About Unity Synthetic Data

1. [Unity Computer Vision Datasets](https://unity.com/products/computer-vision)
2. [Overview on how UCVD works](docs/how-ucvd-works.md)
3. [Unity Perception](https://github.com/Unity-Technologies/com.unity.perception)
4. [Create your own assets on UCVD](docs/create-ucvd-assets.md)
