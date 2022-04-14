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

Checkout our example at - [Demo](https://huggingface.co/spaces/unity3d/Indoor-Pet-Detection)

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

### Results

<table>
<tr>
  <td>Pre-training</td>
  <td>Fine tune(real data)</td>
  <td>AP</td>
  <td>Data generation time(mins)</td>
</tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_imagenet_0k_synthetic.pth">ImageNet + no synthetic</a>
  </td><td>1200</td><td>51.16</td><td>---</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_imagenet_5k_synthetic.pth">ImageNet + 5k synthetic </a>
    </td><td>1200</td><td>57.18</td><td>33</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_imagenet_10k_synthetic.pth">ImageNet + 10k synthetic </a>
  </td><td>1200</td><td>58.42</td><td>35</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_imagenet_40k_synthetic.pth">ImageNet + 40k synthetic </a>
  </td><td>1200</td><td>63.03</td><td>50</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_imagenet_100k_synthetic.pth">ImageNet + 100k synthetic </a>
  </td><td>1200</td><td>65.4</td><td>84</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_scratch_0k.pth">Scratch + no synthetic </a>
  </td><td>1200</td><td>23.16</td><td>---</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_scratch_5k.pth">Scratch + 5k  synthetic </a>
  </td><td>1200</td><td>36.16</td><td>33</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_scratch_10k.pth">Scratch + 10k synthetic </a>
  </td><td>1200</td><td>36.97</td><td>35</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_scratch_40k.pth">Scratch + 40k synthetic </a>
  </td><td>1200</td><td>47.3</td><td>50</td></tr>
<tr><td>
  <a href="https://github.com/Unity-Technologies/Indoor-Pet-Detection/releases/download/v0.1.1-ckpt/checkpoints_model_final_scratch_100k.pth">Scratch + 100k synthetic </a>
  </td><td>1200</td><td>53.78</td><td>84</td></tr>
</table>
