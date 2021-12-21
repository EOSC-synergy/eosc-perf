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

        stage('SQA baseline dynamic stages') {
            environment {
                // get jenkins user id and group
                jenkins_user_id = sh (returnStdout: true, script: 'id -u').trim()
                jenkins_user_group = sh (returnStdout: true, script: 'id -g').trim()            
            }
            steps {
                // execute 'backend' pipeline
                script {
                    projectConfig = pipelineConfig(configFile: env.sqa_config_backend)
                    buildStages(projectConfig)
                }
                // execute 'frontend' pipeline
                script {
                    projectConfig = pipelineConfig(configFile: env.sqa_config_frontend)
                    buildStages(projectConfig)
                }
            }
            post {
                always {
                    // BE: publish stylecheck (flake8) report:
                    recordIssues(
                        enabledForFailure: true, aggregatingResults: true,
                        tool: pyLint(pattern: 'service_backend/tmp/flake8.log', 
                                     reportEncoding:'UTF-8',
                                     name: 'BE - CheckStyle')
                    )

                    // BE: publish coverage report (only BE, works??):
                    cobertura(
                        coberturaReportFile: 'service_backend/tmp/be-coverage.xml', 
                        enableNewApi: true,
                        failUnhealthy: false, failUnstable: false, onlyStable: false
                    )

                    // BE: publish bandit report:
                    // according to https://vdwaa.nl/openstack-bandit-jenkins-integration.html
                    // XML output of bandit can be parsed as JUnit
                    recordIssues(
                        enabledForFailure: true, aggregatingResults: true,
                        tool: junitParser(pattern: 'service_backend/tmp/bandit.xml', 
                                           reportEncoding:'UTF-8',
                                           name: 'BE - Bandit')
                    )
                    // FE: publish codestyle:
                    // replace path in the docker container with relative path
                    sh "sed -i 's/\\/perf-testing/./gi' frontend-js/eslint-codestyle.xml"
                    recordIssues(
                        enabledForFailure: true, aggregatingResults: true,
                        tool: checkStyle(pattern: 'frontend-js/eslint-codestyle.xml', 
                                         reportEncoding:'UTF-8',
                                         name: 'FE - CheckStyle')
                    )

                    // publish BE+FE coverage reports:
                    // service_backend/tmp/be-coverage.xml +
                    // frontend-js/coverage/fe-cobertura-coverage.xml:
                    sh "cd frontend-js/coverage && mv cobertura-coverage.xml fe-cobertura-coverage.xml && cd -"
                    publishCoverage(adapters: [coberturaAdapter(path: '**/*-coverage.xml')],
                                    tag: 'Coverage', 
                                    failUnhealthy: false, failUnstable: false
                    )
                    // FE: publish the output of npm audit:
                    recordIssues(
                        enabledForFailure: true, aggregatingResults: true,
                        tool: issues(name: 'FE - NPM Audit', pattern:'frontend-js/npm-audit.json'),
                    )
                }                 
                cleanup {
                    cleanWs()
                }
            }
        }
    }
}
