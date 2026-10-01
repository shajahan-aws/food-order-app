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
                    // Existing conflting containers ko force-remove karke up karo
                    sh 'docker-compose down --remove-orphans || true'
                    sh 'docker rm -f food-db food-order-api || true'
                    sh 'docker-compose up -d --build'
                }
            }
        }

        stage('Wait for Services') {
            steps {
                echo 'Waiting for application and database to initialize...'
                sh 'sleep 10'
            }
        }

        stage('Test & Verify Application') {
            steps {
                echo 'Testing application...'
                // AAPKE TEST COMMANDS YAHAN AAYENGE
                // Example: sh 'curl http://localhost:5000/ || exit 1'
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
            sh 'docker-compose down --remove-orphans || true'
        }
    }
}