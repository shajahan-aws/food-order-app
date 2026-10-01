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
                echo 'Running live endpoint tests on application...'
                script {
                    // Test 1: Check Order API directly
                    sh 'curl -f http://localhost:5000/ || exit 1'
                    
                    // Test 2: Check Nginx Reverse Proxy
                    sh 'curl -f http://localhost:80/ || exit 1'
                }
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