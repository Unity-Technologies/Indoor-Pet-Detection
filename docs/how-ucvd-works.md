## Overview of how UCVD works

<p align="center">
<image src="images/ucvd-overview.png" width="600">
</p>

### Domain Randomization

Deep learning in the computer vision area always needs a large amount of data, while there hardly exist such datasets in many industrial applications for reasons of data privacy, confidentiality, and others. Synthetic data provides a way to achieve clean, unlimited, and high-quality datasets so that machine learning models can be well-trained in the synthetic domain. The model trained with synthetic data is known to have a domain gap to the real world. Domain randomization aims to create variability in the datasets in order to enhance the training of deep neural networks. The randomization forces the neural network to learn the essential features of the object of interest and help to generalize the model to real-world applications.

Unity Computer Vision datasets (UCVD) service utilizes the [Unity Perception package](https://github.com/Unity-Technologies/com.unity.perception) to generate large-scale datasets with domain randomization. The package randomizes the parameters of the environment ("Template") and objects ("Assets") in the scene based on predefined rules and distributions ("Randomizers"). Some of the randomizations include the placement of the camera, the pose and scale of objects, the lighting in the scene, and so on. In each iteration, UCVD uses a set of randomizers to place the assets into the environment and randomize the parameters in the scene. At the end of every iteration, an image will be captured from the camera in the scene and stored with ground-truth information about the labeled objects.

Read [this tutorial](https://github.com/Unity-Technologies/com.unity.perception/blob/main/com.unity.perception/Documentation~/Randomization/Index.md) for more information about the domain randomization in UCVD and Unity Perception package.

### Template

A UCVD **template** is a Unity data generator that enables you to quickly generate a dataset for a specific kind of environment with randomization parameters specific to that environment. The **environment** is the 3D models in the background of generated images, like home interior or retail shelves, where the assets and objects are placed.

A **randomizer** is a set of rules that defines the placement of assets in the environment and varies the parameters of the scene in each frame, such as the color of lighting and scales of objects. Randomizers are configurable. You can customize the range of parameters in the configuration and the parameters will be randomized with the given distribution in each image. Read [this document](https://github.com/Unity-Technologies/com.unity.perception/blob/main/com.unity.perception/Documentation~/Randomization/Index.md#randomizers) for more information about the randomizers.

### Asset and Asset Role

**Assets** are 3D models of the objects of interest that you want to be in the environment and rendered as part of the dataset. They could be the objects that your computer vision models are trained to detect. At this time, UCVD only accepts FBX files with embedded textures and animations as assets. The assets can be uploaded as public if you want all UCVD users to view and use them; otherwise, you can keep them private to yourself. Each asset can have **labels**, and UCVD will capture the ground-truth information along with each captured frame. Read [this tutorial](create-ucvd-assets.md) for more information about creating 3D content and assets on UCVD.

**Asset Role** is defined in the template, and it is the bridge between assets and randomizers. Before generating the synthetic dataset, each randomizer will find all the assets attached with a certain asset role so that it will only randomize the parameters of those assets. For example, in the following image, the foreground and background randomizers in the template randomize the assets with different rules. The background randomizer only updates the textures and materials of the assets, and the foreground randomizer changes the positions and rotations of the objects. Each asset is allowed to contain one or more asset roles. The dog asset contains the foreground role so that it will be only randomized by the foreground randomizer. The table asset will be updated only by the background randomizer since it contains the background role. The sofa asset, which contains both foreground and background roles, will be randomized by both randomizers. For more information about the asset role, read [the data generation tutorial](dataset-generation-and-configuration.md) of the Indoor Pet Detection.

<p align="center">
<image src="images/ucvd-asset-role.png" width="600">
</p>
