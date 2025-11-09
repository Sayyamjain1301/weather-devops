pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo "🔄 Pulling latest code from GitHub..."
                git branch: 'main', url: 'https://github.com/Sayyamjain1301/weather-devops.git'
            }
        }

        stage('Trigger Local Build') {
            steps {
                echo "🚀 Triggering local build manually..."
                echo "Please run these commands in your terminal:"
                echo "1️⃣ eval \$(minikube docker-env)"
                echo "2️⃣ docker build -t weather-app:latest ."
                echo "3️⃣ kubectl apply -f k8s/flask-deployment.yaml"
                echo "✅ Then verify using: kubectl get pods"
            }
        }
    }

    post {
        success {
            echo "🎉 Jenkins pipeline executed successfully!"
        }
        failure {
            echo "❌ Jenkins pipeline failed. Check logs!"
        }
    }
}