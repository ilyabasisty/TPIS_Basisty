pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'pip install -r requirements.txt --break-system-packages'
            }
        }
        stage('test') {
            steps {
                sh 'python3 -m pytest'
            }
        }
    }
}