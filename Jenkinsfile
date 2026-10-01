pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'food_ordering'
    }

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
                    sh 'docker compose down || true'
                    sh 'docker compose up --build -d'
                }
            }
        }

        stage('Wait for Services') {
            steps {
                script {
                    echo 'Waiting for Nginx & Order API to respond...'
                    sh '''
                    for i in {1..12}; do
                      if curl -s http://localhost/health | grep -q "healthy"; then
                        echo "API is up and healthy!"
                        exit 0
                      fi
                      echo "Waiting for service... ($i/12)"
                      sleep 5
                    done
                    echo "Service health check timed out!"
                    exit 1
                    '''
                }
            }
        }

        stage('Test & Verify Application') {
            steps {
                script {
                    echo 'Creating a test order via Nginx proxy...'
                    sh '''
                    CREATE_RES=$(curl -s -X POST http://localhost/orders \
                      -H "Content-Type: application/json" \
                      -d '{"item_name": "Chicken Biryani", "quantity": 2}')
                    
                    echo "Create Order Response: $CREATE_RES"
                    
                    if ! echo "$CREATE_RES" | grep -q "Chicken Biryani"; then
                      echo "FAILED: Order creation failed"
                      exit 1
                    fi
                    '''

                    echo 'Retrieving orders via API...'
                    sh '''
                    GET_RES=$(curl -s http://localhost/orders)
                    echo "Get Orders Response: $GET_RES"
                    
                    if ! echo "$GET_RES" | grep -q "Chicken Biryani"; then
                      echo "FAILED: Order missing from DB read query"
                      exit 1
                    fi
                    echo "VERIFICATION PASSED: Order saved and retrieved successfully!"
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed! Displaying container logs for debugging...'
            sh 'docker compose logs'
        }
        always {
            echo 'Cleaning up application containers while retaining DB volume...'
            sh 'docker compose down'
        }
    }
}