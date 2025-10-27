pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: '<YOUR_GITHUB_REPO_URL>'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t weather-devops-app .'
            }
        }
        stage('Run Container') {
            steps {
                sh 'docker rm -f weather-devops-run || true'
                sh 'docker run -d --name weather-devops-run -p 5000:5000 weather-devops-app'
            }
        }
    }
}
