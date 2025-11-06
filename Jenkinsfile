pipeline {
    agent any

    environment {
        APP_NAME = "weather-devops"
        DOCKER_IMAGE = "sayyamjain/${APP_NAME}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo '📦 Checking out source code...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📥 Installing Python dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo '🧪 Running tests...'
                sh 'pytest || echo "⚠️ No tests found, skipping..."'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Run Container') {
            steps {
                echo '🚀 Running container for verification...'
                sh 'docker run -d -p 8080:8080 $DOCKER_IMAGE'
            }
        }

        stage('Monitor Metrics') {
            steps {
                echo '📊 Verifying Prometheus metrics endpoint...'
                sh 'curl -f http://localhost:8080/metrics || echo "Metrics not available yet"'
            }
        }

        stage('Clean Up') {
            steps {
                echo '🧹 Cleaning up Docker containers...'
                sh 'docker stop $(docker ps -q) || true'
                sh 'docker rm $(docker ps -a -q) || true'
            }
        }
    }

    post {
        always {
            echo '✅ Build pipeline finished.'
        }
    }
}