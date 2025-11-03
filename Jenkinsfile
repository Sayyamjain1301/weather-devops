pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'weather-devops'
        REPO_URL = 'https://github.com/Sayyamjain1301/weather-devops.git'
    }

    stages {

        stage('Declarative: Checkout SCM') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Checkout') {
            steps {
                echo 'Pulling latest code from GitHub...'
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t weather-devops .'
            }
        }

        stage('Run Container') {
            steps {
                echo 'Running Docker container...'
                sh '''
                docker ps -q --filter "name=weather-devops" | grep -q . && docker stop weather-devops || true
                docker ps -aq --filter "name=weather-devops" | grep -q . && docker rm weather-devops || true
                docker run -d -p 10000:10000 --name weather-devops weather-devops
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Build and deployment successful!'
        }
        failure {
            echo '❌ Build failed. Please check logs.'
        }
    }
}
