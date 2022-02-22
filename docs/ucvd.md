### UCVD

#### Unity Dashboard

Open your browser and go to [Unity Dashboard](https://dashboard.unity3d.com/). If this is your first time using the Dashboard, it will ask you to log in. If you haven't had a Unity account, click the "Create account" button and follow the instructions to create an account. 

Sign in to the Unity Dashboard after setting up the account. In the Unity Dashboard, click the **"DevOps"** on the left column of the webpage, and then choose **CV-Datasets -> Create Dataset**.

#### Setup UCVD Auth
   1. Follow [UCVD Guide](http://doesnot-exist-yet.com) to get the API Token. You will be using this for UCVD APIs.
   2. Generate a dataset on UCVD # TODO: switch over to SDK later
   3. Get the runID, and set it to the environment variable `UNITY_CVD_RUN_ID`.
   4. Make sure you have the real world data from [here]() in `data/real/`.
