## Dataset Generation

**Table of Contents**

  - [Requirements](#requirements)
  - [Generate Synthetic Data](#generate-synthetic-data)
    - [Select a Template](#select-a-template)
    - [Select Assets](#select-assets)
    - [Object Labeling](#object-labeling)
    - [Randomizers](#randomizers)
    - [Data Generation Settings](#data-generation-settings)
  - [Proceed to Setup Training Environment](#proceed-to-training)

---

### Requirements

Unity Computer Vision Datasets (UCVD) service provides data generation at scale on Cloud. To use UCVD, you are asked to have a Unity project associated with a Unity ID and organization. If you haven't had a Unity project, please follow [the instructions](ucvd.md) to create a Unity account and set up a Unity project via the [Unity Dashboard](https://dashboard.unity3d.com/).

---

### Generate Synthetic Data

#### Select a Template

> Note: Template is a Unity project pre-built to help bootstrap your dataset generation work. It provides the environments where the assets and objects are placed, such as home and retail shelves. In addition, the template contains structure and logic for the placement of assets and randomization of object and scene variables.

1. Navigate to the [UCVD Dashboard](https://dashboard.unity3d.com/computer-vision-datasets) in your browser, and the webpage shows as the image below.

1. Click the **DevOps** in the left column and choose the **CV Datasets > Create dataset** in the second to the left column.

	> Note: There are three templates that are publicly offered, and each template provides the environment in the generated images. In this example, we are going to choose the Home Interior template as our environment of data.

	![](images/navigate-to-templates.png)

	> Note: Users could generate as many as 10,000 free images for each [Unity organization](https://id.unity.com/organizations). The available frames are displayed in the **Frame available** section above the templates. If you need to generate more data, please contact <datamaker-support@unity3d.com>.

	> ![](images/available-frames.png)

1. Click the **Version: Latest** button and confirm that you are using version **3.0.0**.

	> Note: All the UCVD templates are versioned. Version 3.0.0 of the Home Interior template is capable to randomize the assets by their embedded animations.

	<img src = "images/template-version-1.png" width ="400" /> <img src = "images/template-version-2.png"  width ="400"/>

1. Click **Create** button of the Home Interior template

#### Select Assets

> Note: Assets are 3D models of the objects of interest that you want rendered as part of the dataset. These would be the objects that your computer vision models would be trained to detect. At this time, UCVD only support FBX files with embedded textures and animations.

> Note: The Home Interior template provides empty homes with furniture, but there are no people or pets in it, so we need to add pets into the selected environment. In this example, we are going to only place dogs into the houses. If you need to place your own pets, such as cats or other small mammals, the UCVD accepts custom FBX assets and you could upload them.

1. In the webpage as shown below, type `unity_dog` in the search bar to filter assets by their names.

	> Note: We offered 11 breeds of dogs: _Doberman_, _Husky_, _Labrador_, _Bull Terrier_, _Dalmatian_, _Pitbull_, _Collie_, _Corgi_, _JR Terrier_, _Akita_, and _Golden Retriever_. You could select all breeds by marking the checkbox in the header of the asset table.

	![](images/select-assets.png)

1. Click the **Modify roles** button and you will see a popup window as the following image.

	> Note: This window is to assign asset roles to the selected assets. The asset roles are defined by the template, which is used to link the assets and randomizers that will be configured in the later steps. The Home Interior template only has a single asset role: "foreground".

1. Click the **foreground** box in the popup window and it will be moved to the **Added** box.

1. Click the **Close** button to close the floating window.

	![](images/modify-roles.png)

1. After closing the popup window, you will see the roles are assigned in right column of the asset table, as shown in the image below. Click the **Next** button on the top-right corner of the dashboard.

	![](images/role-assigned-assets.png)

#### Object Labeling

1. Click the dropdown box. In the three labeling modes, choose **"Custom Configuration"**.

	> Note: This step is to set up object labeling so that the generated dataset contains labels for each object, like furniture and dog. The Home Interior template contains a set of default labels for the furniture, such as _Table\_Dining_ and _Bookcase_, but it does not have the label for the dog assets, so we need to customize the labels.

	![](images/select-labeling-mode.png)

1. In the popup window, click "Include defaults".

	> Note: This will add all the default furniture labels to all the labelers.

	![](images/include-default-labels.png)

1. In the webpage as the following image, choose **BoundingBox2DLabeler**, mark the checkbox of the **dog** label, and click the **Apply** button. You will see the **dog** label moved to the right column.

1. Repeat the above step on all the other labelers: _InstanceSegmentationLabeler_, _SemanticSegmentationLabeler_, _BoundingBox3DLabeler_, and _ObjectCountLabeler_.

	![](images/add-dog-label.png)

1. Click the **Next** button, and then click **Save & Next** button in the popup window to continue.

#### Randomizers

> Note: A set of randomizers are used to introduce variety into the generated dataset. The Home Interior template provides five randomizers to randomize different factors in the data. You could unfold each randomizer and view the descriptions. In this example, we will only update the parameters in the **Foreground Object Placer** and keep all the other randomizers with default configurations. In the process of data generation, the foreground object placer will find all assets with the "foreground" role and randomly place them in the home.

![](images/foreground-randomizer.gif)

1. Expand the **Foreground Object Placer > Scalar**, and configure the randomizer using the following values.

	| Parameter | Value | Description |
	| --------- | ----- | ----------- |
	| Use Physics to Place Objects | false | Disable physics engine and use ray-based method to place objects (dogs) |
	| Freeze Rotation around X-Axis | true | Disable dog rotation around X-Axis (Pitch) |
	| Freeze Rotation around Y-Axis | false | Enable dog rotation around Y-Axis (Yaw) |
	| Freeze Rotation around Z-Axis | true | Disable dog rotation around Z-Axis (Roll) |
	| Randomize Rotation | true | Enable to randomize the rotation of objects (objects) |
	| Minimum Distance of Placed Objects to the Camera | 0.1 | Minimum distance between the placed objects to the camera |
	| Normalize Object Sizes | false | Disable the normalization of object sizes |
	| Confinement of Placing Objects in the Camera View | 1.0 | Allows to place objects anywhere in the image. Objects will be placed closer to the center of the image if the value is less than 1.0 |
	| Normalized Object Size | 0.5 | This value does not matter since it is disabled |
	| Uniform Sampling | Min: 1, Max: 10 | Randomize the number of objects (dogs) in the field of view |

1. Make sure the **Object Animation Randomizer** is enabled

	> Note: The dog assets contain animations of dog poses, such as walking and sitting. The object animation randomizer here is to introduce a variety of dog poses in the generated datasets.

	![](images/object-animation-randomizer.png)

1. Click the **Next** button.

#### Data Generation Settings

1. Expand the **Settings** box, and set the parameters using the following values

	| Parameter | Value |
	| --------- | ----- |
	| Frames | 10000 |
	| Run Name | Indoor-Pet-Detection |
	| Output Format | Coco |

	![](images/data-generation-settings.png)

1. Click the **Create** button and then click the **continue** in the popup window

	![](images/confirm-data-generation.png)

> Note: The data generation will be triggered after this step. The whole process may take 30 minutes to complete. You can check the status of the generation in **DevOps > CV Datasets > Datasets**.

---

### Proceed to [Setup Training Environment](setup-training-environment.md)
