
@Library("PipelineLibrary") _

env.JOB_NODE_NAME = 'aws-node-00'




node('aws-node-00') {
    ansiColor('xterm') {
        environment {
            JOB_DEFINITION = 'Test'
        }

        ws(env.THIS_WORKSPACE) {


            stage('Set default workspace') {
                echo $WORKSPACE
                echo env.THIS_WORKSPACE
            }
            stage('Retrieve scm vars') {
                def checkoutVars = checkout scm
                def commit_id = checkoutVars.GIT_COMMIT
                env.GIT_COMMIT = checkoutVars.GIT_COMMIT
                env.GIT_BRANCH = checkoutVars.GIT_BRANCH
                env.GIT_LOCAL_BRANCH = checkoutVars.GIT_LOCAL_BRANCH
                env.GIT_PREVIOUS_COMMIT = checkoutVars.GIT_PREVIOUS_COMMIT
                env.GIT_URL = checkoutVars.GIT_URL
            }

            stage('Checkout scm') {
                checkout scm
            }

            stage('Checkout ansible repo') {
                checkoutRepo('https://github.com/BobbyShaftoe/Ansaform.git')
            }

            stage('Download Terraform') {

                sh "curl -o $WORKSPACE/terraform https://releases.hashicorp.com/terraform/0.12.4/terraform_0.12.4_linux_amd64.zip"
            }

            stage('Setup Check') {
                setupCheck {}
            }

        }
    }
}

