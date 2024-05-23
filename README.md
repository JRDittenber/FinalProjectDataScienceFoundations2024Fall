# FinalProjectDataScienceFoundations2024Fall
Classification and computer vision final problem 

# US-Visa-Approval-Prediction

## Git Commands

### Initialize the Git Repository
Start by initializing a Git repository in your project directory. This creates a new Git repository, which will track changes to your project files.

### Add Files to Staging
Add all project files to the staging area, which prepares them to be committed. This step ensures that the changes you made are ready to be saved to the repository.

### Commit Changes
Save the changes to the repository with a descriptive message about what has been done. This step creates a snapshot of your project at a specific point in time.

### Push to Remote Repository
Upload your local repository to a remote repository like GitHub. This allows you to share your code and collaborate with others.

## How to Run the Project

### Create a Virtual Environment
Set up a Python virtual environment to manage your project’s dependencies separately from other projects. This helps avoid conflicts between different projects' requirements.

### Activate the Virtual Environment
Activate the virtual environment so that your project uses the specific dependencies listed in it.

### Install Dependencies
Install all necessary packages and libraries specified in the `requirements.txt` file. These dependencies are crucial for running your project.

### Run the Main Python Script
Execute the main script (`app.py`) to start the application. This script typically contains the core logic of your project.

## Workflow

### Clone the Repository
Copy the project repository from GitHub to your local machine. This step allows you to work on a local copy of the project.

### Create Virtual Environment
Create a virtual environment for managing your project dependencies.

### Install Dependencies
Use the `requirements.txt` file to install all required Python packages.

### Prepare Data
Load the dataset and perform any necessary preprocessing steps, such as cleaning the data and handling missing values.

### Train Model
Develop a logistic regression model using the prepared data. This involves selecting features, splitting the data into training and testing sets, and training the model.

### Evaluate Model
Assess the model's performance using metrics such as accuracy, precision, and recall. This helps determine how well the model predicts outcomes.

### Deploy Application
Set up the application for deployment so it can be accessed and used by others. This involves packaging the application and preparing it for a production environment.

### Run Application
Execute the application to make predictions based on user inputs or new data.

## Export the Environment Variable
Define and set any necessary environment variables to ensure the application runs correctly in different environments. Environment variables are used to configure settings without hardcoding them into your application.

# AWS-CICD-Deployment-with-Github-Actions

### 1. Login to AWS Console
Access the AWS Management Console using your AWS account credentials. The console is a web-based interface for managing AWS services.

### 2. Create IAM User for Deployment

#### Navigate to IAM (Identity and Access Management)
IAM is a web service for securely controlling access to AWS services.

#### Create a New User
Set up a new IAM user with programmatic access to interact with AWS services via the AWS CLI. Programmatic access allows the user to perform AWS actions using command-line tools.

#### Attach Policies
Attach policies to the IAM user to grant permissions. For deploying Docker images, attach the `AmazonEC2ContainerRegistryFullAccess` policy, which allows the user to interact with the Elastic Container Registry (ECR).

### 3. Create ECR Repository to Store/Save Docker Image

#### Navigate to ECR (Elastic Container Registry)
ECR is a managed Docker container registry that makes it easy to store, manage, and deploy Docker container images.

#### Create a New Repository
Set up a new repository to store your Docker images. Note the repository URI, which will be used to push images to ECR. A Docker image is a lightweight, standalone, and executable package that includes everything needed to run a piece of software, including the code, runtime, libraries, and dependencies.

### 4. Create EC2 Machine (Ubuntu)

#### Navigate to EC2 (Elastic Compute Cloud)
EC2 provides scalable computing capacity in the AWS cloud. It allows you to launch virtual servers, known as instances, to run applications.

#### Launch Instance
Create a new EC2 instance using the Ubuntu Server image. Ubuntu is a popular Linux distribution that is widely used for cloud deployments.

#### Configure Security Group
Set up security rules to allow SSH access and other necessary permissions. A security group acts as a virtual firewall for your instance to control incoming and outgoing traffic.

#### Key Pair
Generate or use an existing key pair to securely connect to your instance. A key pair consists of a public key and a private key, which are used to encrypt and decrypt login information.

### 5. Open EC2 and Install Docker in EC2 Machine

#### Connect to EC2 Instance
Use SSH to connect to your EC2 instance. SSH (Secure Shell) is a protocol for securely accessing remote computers.

#### Update Package Lists
Update the list of available packages and their versions. This ensures you have the latest updates and security patches.

#### Install Docker
Install Docker to manage and deploy applications within containers. Docker containers allow you to package applications and their dependencies in a consistent and reproducible manner.

#### Start Docker Service
Ensure Docker is running and set it to start on boot. This allows Docker to be ready whenever your instance is running.

### 6. Configure EC2 as Self-Hosted Runner

#### GitHub Actions Runner Setup
Follow GitHub’s instructions to set up your EC2 instance as a self-hosted runner. This allows GitHub Actions to run on your EC2 instance.

#### Register Runner
Register the runner with your GitHub repository so that it can execute your CI/CD workflows. Continuous Integration (CI) and Continuous Deployment (CD) workflows automate the process of testing and deploying your code.


### Open EC2 and Install 
```bash
sudo apt-get update -y

sudo apt-get upgrade

#required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker
```
### 7. Setup GitHub Secrets

#### Navigate to GitHub Repository Settings
Go to the settings page of your GitHub repository.

#### Add Secrets
Add the following secrets to enable AWS CLI commands and Docker operations:
- `AWS_ACCESS_KEY_ID`: The access key ID for your AWS account. This is used to authenticate AWS CLI requests.
- `AWS_SECRET_ACCESS_KEY`: The secret access key for your AWS account. This is used together with the access key ID to sign AWS CLI requests.
- `AWS_DEFAULT_REGION`: The default region for AWS services (e.g., `us-west-2`). This specifies the AWS region where your resources are located.
- `EC2_ID`: The ID of your EC2 instance. This is used to identify your instance within AWS.




citation : project based on Bappy Ahmed - with MIT License
