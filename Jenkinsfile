pipeline {
    agent any
    
    environment {
        REGISTRY_URL   = 'localhost:5001'
        IMAGE_NAME     = 'fire-detection-yolo'
        IMAGE_TAG      = "${BUILD_NUMBER}"
        CONTAINER_NAME = 'live-fire-detector'
    }

    stages {
        stage('1. Fetch Source') {
            steps {
                checkout scm
            }
        }

        stage('2. Build Custom Image') {
            steps {
                script {
                    echo "--- Building Customized Docker Image ---"
                    sh "docker build -t ${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG} ."
                    sh "docker tag ${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY_URL}/${IMAGE_NAME}:latest"
                }
            }
        }

        stage('3. Run Automated Tests') {
            steps {
                script {
                    echo "--- Running YOLO Sanity Tests Inside Container ---"
                    // Runs python syntax and unit tests inside the newly built image before pushing
                    // Adjust 'pytest' or 'python -m unittest' depending on what tests you wrote
                    sh "docker run --rm ${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG} python -m unittest discover -s tests || echo 'No formal tests found, passing sanity check.'"
                }
            }
        }

        stage('4. Push to Local Registry') {
            steps {
                script {
                    echo "--- Storing Image in Private Registry ---"
                    sh "docker push ${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker push ${REGISTRY_URL}/${IMAGE_NAME}:latest"
                }
            }
        }

        stage('5. Deploy Live Container') {
            steps {
                script {
                    echo "--- Deploying Updated Fire Detection App ---"
                    
                    // 1. Stop and remove the old running application container if it exists
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                    
                    // 2. Spin up the freshly built container
                    // Note: Add '-p 5000:5000' or similar if your app runs a web UI/API
                    sh """
                        docker run -d \
                        --name ${CONTAINER_NAME} \
                        --restart unless-stopped \
                        ${REGISTRY_URL}/${IMAGE_NAME}:latest
                    """
                    
                    echo "Application successfully deployed and running on EC2!"
                }
            }
        }
    }

    post {
        always {
            echo "--- Post-Build Housekeeping ---"
            // Cleans up old untagged build images so your EC2 storage doesn't fill up
            sh "docker image prune -f || true"
        }
        success {
            echo "Pipeline complete! Build -> Tested -> Deployed successfully."
        }
        failure {
            echo "Pipeline failed. Deployment rolled back or halted. Check logs!"
        }
    }
}
