pipeline {
    agent any

    environment {
        // Uses the global credentials established in your Jenkins instance
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred')
        IMAGE_NAME = "yourdockerhubusername/sample-web-app" // Update this line
        IMAGE_TAG = "${env.BUILD_ID}"
    }

    stages {
        stage('Test') { // Set 15: Automated Testing
            steps {
                script {
                    echo "Running unit tests..."
                    bat "pip install -r requirements.txt pytest"
                    bat "pytest tests.py"
                }
            }
        }

        stage('Build & Push Docker Image') { // Set 12 & 15: Build and Push
            steps {
                script {
                    echo "Building Docker image..."
                    bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                    bat "docker build -t ${IMAGE_NAME}:latest ."
                    
                    echo "Pushing to DockerHub..."
                    bat "echo %DOCKERHUB_CREDENTIALS_PSW% | docker login -u %DOCKERHUB_CREDENTIALS_USR% --password-stdin"
                    bat "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                    bat "docker push ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy & Rolling Update') { // Set 12 & 13: Kubernetes Deployment
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    script {
                        echo "Applying manifests..."
                        bat "kubectl apply -f deployment.yaml"
                        bat "kubectl apply -f service.yaml"
                        
                        echo "Triggering Rolling Update with new image..."
                        bat "kubectl set image deployment/sample-web-app web-app-container=${IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Verify Rollout Status') { // Set 13: Verify Deployment
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    script {
                        echo "Waiting for rollout to complete..."
                        // Timeout prevents the pipeline from hanging infinitely if pods crash
                        bat "kubectl rollout status deployment/sample-web-app --timeout=90s"
                    }
                }
            }
        }
    }
    
    post {
        failure { // Set 14: Detect and Troubleshoot Failures
            withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                script {
                    echo "PIPELINE FAILED. Executing automated Kubernetes troubleshooting..."
                    // Fetch deployment events and errors
                    bat "kubectl describe deployment sample-web-app"
                    // Fetch status of the failing pods
                    bat "kubectl get pods -l app=sample-web-app"
                    
                    echo "Rolling back to previous stable version..."
                    bat "kubectl rollout undo deployment/sample-web-app"
                }
            }
        }
        always {
            script {
                bat "docker logout"
            }
        }
    }
}

