pipeline {
    agent { node { label 'test Jenkins agent' } }
    stages {
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