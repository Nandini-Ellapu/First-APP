pipeline {
    agent any

    environment {
        AZURE_USER = "Nandini"                      // Your Azure VM username
        AZURE_HOST = "4.247.23.206"                 // Your Azure VM IP
        APP_DIR = "/home/Nandini/app"               // Ensure correct path
        APP_PORT = "5000"                           // Flask application port
    }

    stages {
        stage('Deploy to Azure VM') {
            steps {
                sshagent(['azure-ssh-login']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${AZURE_USER}@${AZURE_HOST} << EOF
                        cd ${APP_DIR}
                        git pull origin main
                        EOF
                    """
                }
            }
        }

        stage('Restart Application on Azure') {
            steps {
                sshagent(['azure-ssh-login']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${AZURE_USER}@${AZURE_HOST} << EOF
                        sudo pkill -f gunicorn || echo "Gunicorn process not found"
                        cd ${APP_DIR}
                        source venv/bin/activate
                        nohup gunicorn -w 4 -b 0.0.0.0:${APP_PORT} main:app > gunicorn.log 2>&1 &
                        EOF
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Deployment to Azure successful!'
        }
        failure {
            echo '❌ Deployment failed. Check logs.'
        }
    }
}
