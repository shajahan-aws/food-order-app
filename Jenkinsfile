pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build & Start Services') {
            steps {
                script {
                    echo 'Building and starting environment via Docker Compose...'
                    sh 'docker-compose down || true'
                    sh 'docker-compose up -d --build'
                }
            }
        }

        stage('Wait for Services') {
            steps {
                sh 'sleep 10'
            }
        }

        stage('Test & Verify Application') {
            steps {
                echo 'Testing application...'
                // AAPKE TEST COMMANDS YAHAN AAYENGE
                // Example: sh 'curl http://localhost:5000/health || exit 1'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed! Displaying container logs...'
            sh 'docker-compose logs || true'
        }
        always {
            echo 'Cleaning up application containers...'
            sh 'docker-compose down || true'
        }
    }
}