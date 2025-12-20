pipeline {
    agent any

    environment {
        NEXUS_REGISTRY = "13.222.210.181:8083"
        FRONTEND_IMAGE = "bookstore-frontend"
        BACKEND_IMAGE  = "bookstore-backend"
        IMAGE_TAG = "1.0"
    }

    stages {

        stage('Build Frontend Image') {
            steps {
                dir('bookstore-frontend') {
                    sh 'docker build -t $FRONTEND_IMAGE:$IMAGE_TAG .'
                }
            }
        }

        stage('Build Backend Image') {
            steps {
                dir('bookstore-backend') {
                    sh 'docker build -t $BACKEND_IMAGE:$IMAGE_TAG .'
                }
            }
        }

        stage('Tag Images') {
            steps {
                sh '''
                  docker tag $FRONTEND_IMAGE:$IMAGE_TAG $NEXUS_REGISTRY/$FRONTEND_IMAGE:$IMAGE_TAG
                  docker tag $BACKEND_IMAGE:$IMAGE_TAG  $NEXUS_REGISTRY/$BACKEND_IMAGE:$IMAGE_TAG
                '''
            }
        }

        stage('Push Images to Nexus') {
            steps {
                withCredentials([
                  usernamePassword(
                    credentialsId: 'nexus-credentials',
                    usernameVariable: 'NEXUS_USER',
                    passwordVariable: 'NEXUS_PASS'
                  )
                ]) {
                    sh '''
                      echo "$NEXUS_PASS" | docker login $NEXUS_REGISTRY -u "$NEXUS_USER" --password-stdin
                      docker push $NEXUS_REGISTRY/$FRONTEND_IMAGE:$IMAGE_TAG
                      docker push $NEXUS_REGISTRY/$BACKEND_IMAGE:$IMAGE_TAG
                    '''
                }
            }
        }
        stage('Configure kubectl') {
        steps {
            sh '''
            aws eks update-kubeconfig \
                --region us-east-1 \
                --name bookstore-eks
            '''
            }
        }

        stage('Deploy to EKS') {
      steps {
        sh '''
            kubectl apply -f k8s/namespace.yml
            kubectl apply -f k8s/backend-deploy.yml
            kubectl apply -f k8s/backend-service.yml
            kubectl apply -f k8s/frontend-deploy.yml
            kubectl apply -f k8s/frontend-service.yml

        '''
      }
    }
  }
}
