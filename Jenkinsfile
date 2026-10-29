pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred')
        IMAGE_NAME = "aryandash77/sample-web-app" 
        IMAGE_TAG = "${env.BUILD_ID}"
    }

    stages {
        stage('Build & Push Docker Image') { 
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

        stage('Deploy with Readiness Probe') { 
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    script {
                        echo "Applying Deployment with Readiness Probe..."
                        bat "kubectl apply -f Deployment.yaml"
                        bat "kubectl apply -f Service.yaml"
                        
                        echo "Updating image to trigger new pods..."
                        bat "kubectl set image deployment/sample-web-app web-app-container=${IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Verify Probe Status') { 
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    script {
                        echo "Waiting for pods to pass the readiness probe..."
                        bat "kubectl rollout status deployment/sample-web-app --timeout=90s"
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                bat "docker logout"
            }
        }
    }
}

