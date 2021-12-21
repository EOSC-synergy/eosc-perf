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

        stage('SQA baseline dynamic stages (backend)') {
            // may execute this action, only when "service_backend" is changed
            //when { changeset 'service_backend/*'}
            environment {
                jenkins_user_id = sh (returnStdout: true, script: 'id -u').trim()
                jenkins_user_group = sh (returnStdout: true, script: 'id -g').trim()            
            }
            steps {
                script {
                    echo env.jenkins_user_id
                    echo env.jenkins_user_group
                    projectConfig = pipelineConfig(configFile: env.sqa_config_backend)
                    buildStages(projectConfig)
                }
            }
            post {
                always {
                    // publish stylecheck (flake8) report:
                    recordIssues(
                        enabledForFailure: true, aggregatingResults: true,
                        tool: pyLint(pattern: 'service_backend/tmp/flake8.log', 
                                     reportEncoding:'UTF-8',
                                     name: 'BE - CheckStyle')
                    )
                    // publish cobertura report:
                    publishCoverage(adapters: [coberturaAdapter(mergeToOneReport: true, path: '**/*-coverage.xml')],
                                    tag: 'Coverage',  
                                    failUnhealthy: false, failUnstable: false
                    )
                    // publish bandit report:
                    // according to https://vdwaa.nl/openstack-bandit-jenkins-integration.html
                    // XML output of bandit can be parsed as JUnit
                    recordIssues(
                        enabledForFailure: true, aggregatingResults: true,
                        tool: junitParser(pattern: 'service_backend/tmp/bandit.xml', 
                                           reportEncoding:'UTF-8',
                                           name: 'BE - Bandit')
                    )
                }                 
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
                always {
                    // publish codestyle:
                    // replace path in the docker container with relative path
                    sh "sed -i 's/\\/perf-testing/./gi' frontend-js/eslint-codestyle.xml"
                    recordIssues(
                        enabledForFailure: true, aggregatingResults: true,
                        tool: checkStyle(pattern: 'frontend-js/eslint-codestyle.xml', 
                                         reportEncoding:'UTF-8',
                                         name: 'FE - CheckStyle')
                    )

                    // publish cobertura report:
                    sh "cd frontend-js/coverage && mv cobertura-coverage.xml fe-cobertura-coverage.xml && cd -"
                    //cobertura(
                    //    coberturaReportFile: 'frontend-js/coverage/fe-cobertura-coverage.xml', 
                    //    enableNewApi: true,
                    //    failUnhealthy: false, failUnstable: false, onlyStable: false
                    //)
                    publishCoverage(adapters: [coberturaAdapter(mergeToOneReport: true, path: '**/*-coverage.xml')],
                                    tag: 'Coverage', 
                                    failUnhealthy: false, failUnstable: false
                    )
                    // publish the output of npm audit:
                    recordIssues(
                        enabledForFailure: true, aggregatingResults: true,
                        tool: issues(name: 'FE - NPM Audit', pattern:'frontend-js/npm-audit.json'),
                        //qualityGates: [
                        //   [threshold: 100, type: 'TOTAL', unstable: true],
                        //   [threshold: 1, type: 'TOTAL_ERROR', unstable: false]
                        //]
                    )
                }          
                cleanup {
                    cleanWs()
                }
            }
        }
    }
}
