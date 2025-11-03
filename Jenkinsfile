pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "weather-ai-assistant"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'feat/feature-roadmap',
                    url: 'https://github.com/Sayyamjain1301/weather-devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    // Stop and remove any old container if running
                    sh 'docker rm -f weather-ai-container || true'
                    sh 'docker run -d -p 8080:10000 --name weather-ai-container $DOCKER_IMAGE'
                }
            }
        }
    }

    post {
        success {
            echo "✅ Weather AI Assistant deployed successfully on Docker!"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}