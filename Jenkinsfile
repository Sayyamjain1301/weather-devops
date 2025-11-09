pipeline {
    agent any

    environment {
        APP_NAME = 'weather-app'
        K8S_DEPLOYMENT = 'k8s/flask-deployment.yaml'
    }

    stages {

        stage('Checkout') {
            steps {
                echo "🔄 Cloning Git repository..."
                git branch: 'main', url: 'https://github.com/Sayyamjain1301/weather-devops.git'
            }
        }

        stage('Setup Minikube Docker Environment') {
            steps {
                echo "⚙️ Setting up Minikube Docker environment..."
                // Connect Docker CLI inside Jenkins to Minikube’s Docker daemon
                sh '''
                if ! command -v minikube >/dev/null 2>&1; then
                    echo "❌ Minikube not found. Make sure Minikube is installed on the Jenkins node."
                    exit 1
                fi
                eval $(minikube -p minikube docker-env)
                '''
            }
        }

        stage('Build Docker Image using Minikube Docker') {
            steps {
                echo "🐳 Building Docker image inside Minikube environment..."
                sh '''
                eval $(minikube -p minikube docker-env)
                docker build -t ${APP_NAME}:latest .
                '''
            }
        }

        stage('Verify Image') {
            steps {
                echo "🔍 Verifying built Docker image..."
                sh '''
                eval $(minikube -p minikube docker-env)
                docker images | grep ${APP_NAME} || (echo "❌ Image not found!" && exit 1)
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "🚀 Deploying ${APP_NAME} to Kubernetes..."
                sh '''
                kubectl delete deployment ${APP_NAME} --ignore-not-found
                kubectl delete service weather-service --ignore-not-found
                kubectl apply -f ${K8S_DEPLOYMENT}
                '''
            }
        }

        stage('Post-Deployment Check') {
            steps {
                echo "✅ Checking running pods and services..."
                sh '''
                kubectl get pods -o wide
                kubectl get svc
                '''
            }
        }
    }

    post {
        success {
            echo "🎉 Deployment completed successfully! Weather App is live in Minikube!"
        }
        failure {
            echo "❌ Deployment failed. Please check Jenkins logs for details."
        }
    }
}