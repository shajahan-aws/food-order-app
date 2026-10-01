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
                    sh 'docker-compose down --remove-orphans || true'
                    // Pure environment ke puraane containers force-remove karo
                    sh 'docker rm -f food-db food-order-api food-nginx-proxy || true'
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
                // Aapke test commands
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