pipeline {
    agent any

    stages {

        stage('Test') {
            environment {
                JENKINS_TOKEN = credentials('TOKEN')
                AWS_KEY = credentials('ACCESS_KEY')
                AWS_TOKEN = credentials('AWS_TOKEN')
            }
            steps {
                sh "echo ${env.BUILD_ID} on ${env.JENKINS_URL}, '$JENKINS_TOKEN, $AWS_KEY, $AWS_TOKEN'"
            }
        }
    }

}
