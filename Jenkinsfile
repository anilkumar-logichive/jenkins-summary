pipeline {
    agent any

    environment {
        GIT_URL = credentials('GIT_URL')
        JENKINS_USER = "anilkumar_admin"
        JENKINS_TOKEN = credentials('TOKEN')
        S3_BUCKET_NAME = "logichivebuildreport"
        AWS_KEY = credentials('ACCESS_KEY')
        AWS_TOKEN = credentials('AWS_TOKEN')
        SUMMARY_URL = credentials('SUMMARY_URL')
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
                sh 'python3 test_app.py'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, skipOldReports: true, skipPublishingChecks: true, testResults:'**/test_reports/*.xml'
            git 'https://github.com/anilkumar-logichive/jenkins-summary.git'
            sh "echo '$JENKINS_USER' '$JENKINS_TOKEN' ${env.JENKINS_URL} ${env.JOB_NAME} ${env.BUILD_NUMBER} '$S3_BUCKET_NAME' '$AWS_KEY' '$AWS_TOKEN'"
            sh "python3 main.py '$JENKINS_USER' '$JENKINS_TOKEN' ${env.JENKINS_URL} ${env.JOB_NAME} ${env.BUILD_NUMBER} '$S3_BUCKET_NAME' '$AWS_KEY' '$AWS_TOKEN'"
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
