# Deploying an ML Model on AWS using EC2, ECR, and EKS

This project demonstrates an end-to-end workflow for deploying a machine learning model on AWS using Docker, Amazon Elastic Container Registry (ECR), and Amazon Elastic Kubernetes Service (EKS). The model is a Flask-based API for the Iris dataset, containerized using Docker and deployed on AWS EKS.

## Architecture
The deployment consists of the following AWS services:
- **EC2 Instance**: Used for development, building Docker images, and pushing to ECR.
- **ECR (Elastic Container Registry)**: Stores the Docker image.
- **EKS (Elastic Kubernetes Service)**: Manages the Kubernetes cluster.
- **Flask API**: Serves predictions using the deployed ML model.

## Prerequisites
Before starting, ensure you have the following:
- An **AWS account** with necessary IAM permissions.
- An **EC2 instance** with Docker and `eksctl` installed.
- AWS CLI, Docker, and `kubectl` installed on your machine.
- A pre-trained machine learning model (stored as a `.pkl` file).

## Step 1: Set Up EC2 Instance
1. Launch an **EC2 instance** with Ubuntu.
2. Connect to the instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```
3. Install necessary packages:
   ```bash
   sudo apt update && sudo apt install -y docker.io awscli
   ```
4. Start Docker:
   ```bash
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

## Step 2: Clone the Repository
```bash
git clone https://github.com/onehungrybird/ml_aws_kubernetes.git
cd ml_aws_kubernetes
```

## Step 3: Build and Push Docker Image to ECR
1. **Authenticate Docker with AWS ECR:**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account_id>.dkr.ecr.us-east-1.amazonaws.com
   ```
2. **Create an ECR Repository:**
   ```bash
   aws ecr create-repository --repository-name iris-model
   ```
3. **Build the Docker Image:**
   ```bash
   docker build -t iris-model .
   ```
4. **Tag the Image:**
   ```bash
   docker tag iris-model:latest <account_id>.dkr.ecr.us-east-1.amazonaws.com/iris-model:latest
   ```
5. **Push the Image to ECR:**
   ```bash
   docker push <account_id>.dkr.ecr.us-east-1.amazonaws.com/iris-model:latest
   ```

## Step 4: Set Up EKS Cluster
1. **Create an EKS Cluster:**
   ```bash
   eksctl create cluster --name iris-cluster --region us-east-1 --nodegroup-name worker-nodes --nodes 2
   ```
   This may take some time.
2. **Verify the Cluster:**
   ```bash
   aws eks update-kubeconfig --region us-east-1 --name iris-cluster
   kubectl get nodes
   ```

## Step 5: Deploy the Application on EKS
1. **Create Kubernetes Deployment & Service:**
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```
2. **Check if the Pods are Running:**
   ```bash
   kubectl get pods
   ```
3. **Expose the Service:**
   ```bash
   kubectl get services
   ```

## Step 6: Test the Deployment
1. **Get the External IP of the Load Balancer:**
   ```bash
   kubectl get services
   ```
   Look for the `EXTERNAL-IP` under the `LoadBalancer` service.
2. **Make a Test Request:**
   ```bash
   curl -X POST http://<EXTERNAL-IP>:5000/predict -H "Content-Type: application/json" -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
   ```

## Step 7: Clean Up Resources
To avoid incurring unnecessary costs, delete the resources when you're done:
```bash
eksctl delete cluster --name iris-cluster --region us-east-1
aws ecr delete-repository --repository-name iris-model --force
```

## Conclusion
This guide provided an end-to-end implementation of deploying an ML model on AWS using EC2, ECR, and EKS. Now your Flask API is running in a scalable, managed Kubernetes environment on AWS. 🚀

