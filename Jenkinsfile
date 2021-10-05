#!/usr/bin/groovy

@Library(['github.com/indigo-dc/jenkins-pipeline-library@release/2.1.0']) _

def projectConfig

pipeline {
    agent any

    stages {
        stage('Remove old Docker images') {
           steps {
                script {
                    // update config.yml for Jenkins_ID
                    sh "bash docker rmi eoscperf/cicd-images:backend"
                    sh "bash docker rm *perf-backend-testing:latest"
                }
           }
        }
        stage('SQA baseline dynamic stages') {
            steps {
                script {
                    projectConfig = pipelineConfig(configFile: '.sqa-backend/config.yml')
                    buildStages(projectConfig)
                }
            }
            post {
                cleanup {
                    cleanWs()
                }
            }
        }
    }
}
