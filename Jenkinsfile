pipeline {
    agent any

    environment {
        APP_NAME = "weather-app"
        IMAGE_NAME = "weather-app:latest"
        KUBE_DEPLOY_FILE = "k8s/flask-deployment.yaml"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Cloning Git repository...'
                git branch: 'main', url: 'https://github.com/Sayyamjain1301/weather-devops'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh 'eval $(minikube docker-env)'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Verify Image') {
            steps {
                sh 'docker images | grep weather-app || echo "⚠️ Image not found!"'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo '🚀 Deploying to Kubernetes...'
                sh 'kubectl delete deployment $APP_NAME --ignore-not-found=true'
                sh 'kubectl apply -f $KUBE_DEPLOY_FILE'
            }
        }

        stage('Post-Deployment Check') {
            steps {
                echo '🔍 Checking app status...'
                sh 'kubectl get pods -o wide'
                sh 'kubectl get svc weather-service'
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful! Access via: minikube service weather-service --url'
        }
        failure {
            echo '❌ Deployment failed. Check Jenkins logs for details.'
        }
    }
}
