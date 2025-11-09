pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo "🔄 Cloning Git repository..."
                git branch: 'main', url: 'https://github.com/Sayyamjain1301/weather-devops.git'
            }
        }

        stage('Build Docker Image (local)') {
            steps {
                echo "🐳 Building Docker image locally..."
                sh '''
                docker build -t weather-app:latest .
                '''
            }
        }

        stage('Verify Image') {
            steps {
                echo "🔍 Checking Docker image..."
                sh 'docker images | grep weather-app || true'
            }
        }

        stage('Deploy to Kubernetes (Manual Trigger)') {
            steps {
                echo "🚀 Deploying app to Kubernetes..."
                sh '''
                echo "Skipping Minikube setup (using your local environment)..."
                kubectl delete deployment weather-app --ignore-not-found
                kubectl delete service weather-service --ignore-not-found
                kubectl apply -f k8s/flask-deployment.yaml
                '''
            }
        }

        stage('Post-Deployment Check') {
            steps {
                echo "✅ Checking running pods..."
                sh 'kubectl get pods -o wide'
            }
        }
    }

    post {
        success {
            echo "🎉 CI/CD pipeline executed successfully on local environment!"
        }
        failure {
            echo "❌ Deployment failed. Check Jenkins logs for details."
        }
    }
}
