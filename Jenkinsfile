pipeline {
    agent any

    environment {
        APP_NAME = "weather-devops"
        APP_PORT = "10000"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📦 Checking out source code..."
                git branch: 'main', url: 'https://github.com/Sayyamjain1301/weather-devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                sh 'docker build -t ${APP_NAME}:latest .'
            }
        }

        stage('Stop Old Container') {
            steps {
                echo "🧹 Cleaning up old containers..."
                sh """
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true
                """
            }
        }

        stage('Run New Container') {
            steps {
                echo "🚀 Running new container..."
                sh "docker run -d --name ${APP_NAME} -p ${APP_PORT}:${APP_PORT} ${APP_NAME}:latest"
            }
        }
    }

    post {
        success {
            echo "✅ Build & Deployment Successful! Visit: http://localhost:${APP_PORT}"
        }
        failure {
            echo "❌ Build Failed. Check Jenkins logs for details."
        }
    }
}