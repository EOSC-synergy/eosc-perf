#!/usr/bin/groovy

@Library(['github.com/indigo-dc/jenkins-pipeline-library@release/2.1.0']) _

def projectConfig

pipeline {
    agent any

    environment {
        dockerhub_credentials = "o3as-dockerhub-vykozlov"
        cicd_backend_version = "1.0.1"
        dockerhub_cicd_backend = "eoscperf/cicd-images:backend-${cicd_backend_version}"
    }

    stages {
        stage('Build Docker image with tools for CI/CD') {
            when {
                anyOf {
                   changeset 'service_backend/Dockerfile.cicd'
                   changeset 'Jenkinsfile'
                }
            }
            steps{
                checkout scm
                dir('service_backend/') {
                    script {
                        docker.withRegistry('', env.dockerhub_credentials) {
                            def dockerfile = 'Dockerfile.cicd'
                            def cicd_image_backend = docker.build(env.dockerhub_cicd_backend, 
                                                                  "-f ${dockerfile} .")
                            cicd_image_backend.push()
                            cicd_image_backend.push('latest')
                            // logout
                            sh "docker logout"
                        }
                    }
                    
                }
            }
        }

        stage('SQA baseline dynamic stages') {
            environment {
                CICD_BACKEND_VERSION = "${env.cicd_backend_version}"
            }
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
