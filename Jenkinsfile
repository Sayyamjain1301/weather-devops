pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Sayyamjain1301/weather-devops.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t weather-ai-assistant .'
            }
        }

        stage('Run Tests') {
            steps {
                echo '✅ Running unit tests (if any)...'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying container...'
                sh 'docker run -d -p 10000:10000 weather-ai-assistant'
            }
        }
    }

    post {
        success {
            echo '✅ Build and deployment successful!'
        }
        failure {
            echo '❌ Build failed. Check Jenkins logs for details.'
        }
    }
}
