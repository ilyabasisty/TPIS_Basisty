pipeline {
    agent {
        docker { image 'python:3' }
    }
    stages {
        stage('test pip') {
            steps {
                sh 'pip --version'
            }
        }
        stage('build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('test') {
            steps {
                sh 'python3 -m pytest'
            }
        }
    }
}