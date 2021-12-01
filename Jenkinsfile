#!/usr/bin/groovy

@Library(['github.com/indigo-dc/jenkins-pipeline-library@release/2.1.0']) _

def projectConfig

pipeline {
    agent any

    environment {
        sqa_config_backend = ".sqa-backend/config.yml"
        dockerhub_cicd_backend = "eoscperf/cicd-images:backend-1.0.1"
        sqa_config_frontend = ".sqa-frontend/config.yml"
        dockerhub_credentials = "o3as-dockerhub-vykozlov"
    }

    stages {
        stage('Build Docker image with tools for CI/CD (backend)') {
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

        stage('SQA baseline dynamic stages (backend)') {
            // may execute this action, only when "service_backend" is changed
            when { changeset 'service_backend/*'}
            steps {
                script {
                    projectConfig = pipelineConfig(configFile: env.sqa_config_backend)
                    buildStages(projectConfig)
                }
            }
            post {
                cleanup {
                    cleanWs()
                }
            }
        }
        stage('SQA baseline dynamic stages (frontend)') {
            // may execute this action, only when "frontend-js" is changed
            //when { changeset 'frontend-js/*'}
            steps {
                script {
                    projectConfig = pipelineConfig(configFile: env.sqa_config_frontend)
                    buildStages(projectConfig)
                }
            }
            post {
                success {
                  // publish html
                  publishHTML target: [
                      allowMissing: false,
                      alwaysLinkToLastBuild: false,
                      keepAll: true,
                      reportDir: 'frontend-js',
                      reportFiles: 'eslint-codestyle.html',
                      reportName: 'ESlint Codestyle Report'
                    ]
                }            
                cleanup {
                    cleanWs()
                }
            }
        }  
    }
}
