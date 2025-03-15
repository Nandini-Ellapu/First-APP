pipeline {
    agent any

    environment {
        AZURE_USER = "azureuser"                      // Your Azure VM username
        AZURE_HOST = "52.172.25.118"                 // Your Azure VM IP
        APP_DIR = "/home/azureuser/First-APP/app"               // Ensure correct path
        SSH_KEY = "/var/lib/jenkins/azure.pem"      // Path to your Azure private key (like AWS)
        APP_PORT = "5000"                           // Flask application port
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Deploy to Azure') {
            steps {
                script {
                    echo "Copying updated application files to Azure..."
                    sh '''
                    scp -o StrictHostKeyChecking=no -i /var/lib/jenkins/azure.pem -r app/main.py app/templates Nandini@4.247.23.206:/home/azureuser/First-APP/app
                    '''

                    echo "Restarting application on Azure..."
                    sh '''
                    ssh -o StrictHostKeyChecking=no -i /var/lib/jenkins/azure.pem azureuser@4.247.23.206 <<EOF
                    sudo pkill -f gunicorn || echo "Gunicorn process not found"
                    cd /home/azureuser/First-APP/app
                    source venv/bin/activate
                    nohup gunicorn -w 4 -b 0.0.0.0:5000 main:app > gunicorn.log 2>&1 &
                    exit
EOF
                    '''
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
