# 4300 GamePig
![image](https://github.com/user-attachments/assets/598e3af5-0e87-4db8-ac11-05b19211410f)
![image](https://github.com/user-attachments/assets/35bc88f4-6915-4aa8-be1a-478dd6f70c75)


## Contents

- [Summary](#summary)
- [Running Locally](#running-locally)
- [Uploading Large Files](#uploading-large-files)
- [Debugging Some Basic Errors](#debugging-some-basic-errors)
- [Virtual Environments and Dependency Tracking](#virtual-environments-and-dependency-tracking)
- [Troubleshooting](#troubleshooting)
- [General comments from the author](#general-comments-from-the-author)


##DEMO
https://drive.google.com/file/d/1dEoQwssMMbEQnyHvLB0z5Q33XIGZElcY/view

## Running locally
- Ensure that you have Python version 3.10 or above installed on your machine (ideally in a virtual environment). Some of the libraries and code used in the template, as well as on the server end, are only compatible with Python versions 3.10 and above.
  
### Step 1: Set up a virtual environment
Create a virtual environment in Python. You may continue using the one you setup for assignment if necessary. To review how to set up a virtual environment and activate it, refer to A0 assignment writeup.

Run `python -m venv <virtual_env_name>` in your project directory to create a new virtual environment, remember to change <virtual_env_name> to your preferred environment name.

### Step 2: Install dependencies
You need to install dependencies by running `python -m pip install -r requirements.txt` in the backend folder.

## Command to run project locally: 
```flask run --host=0.0.0.0 --port=5000```

## Uploading Large Files 
- Note: This feature is correctly under testing
- When your dataset is ready, it should be of the form of a JSON file of 128MB or less.
  - 128MB is negotiable, based on your dataset requirements
- Click "Upload JSON file" button, choose your file and hit the upload button to send it to your project
- The files are chunked. Any interruption either on the network or client end will require a full file re-upload so be careful
  - In the event your file does not get consistently uploaded due to network issues or takes too long (it really shouldn't) you may request a manual upload
- This JSON file that you upload will always replace your **init.json** file. This means that when you build your project, this file will be automatically imported into your Database and be available to use.

## Debugging Some Basic Errors
- After the build, wait a few seconds as the server will still be loading, especially for larger applications with a lot of setup
- **Do not change the Dockerfiles without permission**
- Sometimes, if a deployment doesn't work, you can try logging out and back in to see if it works
- Alternatively, checking the console will tell you what error it is. If it's a 401, then logging in and out should fix it. 
- If it isn't a 401, first try checking the logs or container status. Check if the containers are alive or not, which could cause issues. If the containers are down, try stopping and starting them. If that does not work, you can report it on ED.
- If data isn't important, destroying and then cloning and re-building containers will usually fix the issue (assuming there's no logical error)
