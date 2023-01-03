pipeline {
    agent {
        docker { image 'python:3.11-alpine' }
    }

    stages {
         stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/anilkumar-logichive/jenkins-test-python.git']]])
            }
        }

        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python test_app.py'
            }
        }
    }

    post {
        always {
            environment {
                JENKINS_USER = credentials('USER')
                JENKINS_TOKEN = credentials('TOKEN')
                S3_BUCKET_NAME = credentials('BUCKET_NAME')
                AWS_KEY = credentials('ACCESS_KEY')
                AWS_TOKEN = credentials('AWS_TOKEN')
            }
            junit allowEmptyResults: true, skipOldReports: true, skipPublishingChecks: true, testResults:'**/test_reports/*.xml'
            git 'https://github.com/anilkumar-logichive/jenkins-summary.git'
            sh "python main.py '$JENKINS_USER' '$JENKINS_TOKEN' ${env.JENKINS_URL} ${env.JOB_NAME} ${env.BUILD_NUMBER} '$S3_BUCKET_NAME' '$AWS_KEY' '$AWS_TOKEN'"
            echo 'The pipeline completed'
        }
        success {
            echo "Build successful"
        }
        failure {
            echo 'Build stage failed'
        }
    }
}
