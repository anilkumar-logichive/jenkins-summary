pipeline {
    agent any

    stages {
        stage('build user') {
            steps {
                wrap([$class: 'BuildUser']) {
                    var name = "${BUILD_USER}"
                }
            }
        }

        stage('Test') {
            environment {
                JENKINS_TOKEN = credentials('TOKEN')
                AWS_KEY = credentials('ACCESS_KEY')
                AWS_TOKEN = credentials('AWS_TOKE')
            }
            steps {
                sh 'echo ${name}, ${env.BUILD_ID} on ${env.JENKINS_URL}, $JENKINS_TOKEN, $AWS_KEY, $AWS_TOKEN'
            }
        }
    }


}
