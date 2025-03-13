pipeline {
    agent any

    environment {
        AZURE_USER = "azureuser"                      // Your Azure VM username (check with `whoami`)
        AZURE_HOST = "4.247.23.206"                   // Your Azure VM IP
        APP_DIR = "Nandini
/home/Nandini"               // Corrected app directory path
        APP_PORT = "5000"                             // Flask application port
    }

    stages {
        stage('Deploy to Azure VM') {
            steps {
                sshagent(['azure-ssh-login']) {      // Use Jenkins SSH credentials
                    sh """
                        ssh -o StrictHostKeyChecking=no ${AZURE_USER}@${AZURE_HOST} '
                        cd ${APP_DIR} && 
                        git pull &&
                        sudo systemctl restart app'
                    """
                }
            }
        }

        stage('Restart Application on Azure') {
            steps {
                sshagent(['azure-ssh-login']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${AZURE_USER}@${AZURE_HOST} '
                        sudo pkill -f gunicorn || echo "Gunicorn process not found"
                        cd ${APP_DIR}
                        source ${APP_DIR}/venv/bin/activate
                        nohup gunicorn -w 4 -b 0.0.0.0:${APP_PORT} main:app > gunicorn.log 2>&1 &'
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment to Azure successful!'
        }
        failure {
            echo 'Deployment failed. Check the logs for details.'
        }
    }
}
