pipeline {
    agent any
    stages {
        // stage('Test') {
        //     agent {
        //         docker {
        //             image 'python:3.5.1'
        //         }
        //     }
        //     steps {
        //         sh 'pip install -r requirements.txt'
        //         sh 'python manage.py makemigrations'
        //         sh 'python manage.py migrate'
        //         sh 'python manage.py test'
        //     }
        //     post {
        //         success {
        //             mail to:"zhaijr@watone.com.cn",
        //             subject:"Test Successful: ${currentBuild.fullDisplayName}",
        //             body: "we passed."
        //         }
        //         failure {
        //             mail to:"zhaijr@watone.com.cn",
        //             subject:"Test Failure: ${currentBuild.fullDisplayName}",
        //             body: "we failed."
        //         }
        //     }
        // }
        stage('Deploy') {
            steps {
                sh 'pwd'
                sh './docker_deploy.sh'
            }
            post {
                success {
                    mail to:"zhaijr@watone.com.cn",
                    subject:"Deploy Successful: ${currentBuild.fullDisplayName}",
                    body: "we passed."
                }
                failure {
                    mail to:"zhaijr@watone.com.cn",
                    subject:"Deploy Failure: ${currentBuild.fullDisplayName}",
                    body: "we failed."
                }
            }
        }
    }
}
