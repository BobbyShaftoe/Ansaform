
@Library("PipelineLibrary") _

env.JOB_NODE_NAME = 'aws-node-00'




node('aws-node-00') {
    ansiColor('xterm') {
        environment {
            JOB_DEFINITION = 'Test'
        }

            stage('Set default workspace') {
                echo env.WORKSPACE

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

                    def out='$(pwd)/Ansaform/terraform'
                    sh "curl https://releases.hashicorp.com/terraform/0.12.4/terraform_0.12.4_linux_amd64.zip -o " + out
                    sh "chmod ugo+x " + out
                    sh "ls -la *"

            }

            stage('Setup Check') {
                setupCheck {}
            }

            stage("Terraform plan") {
                    dir("Ansaform") {

                        sh "terraform init template"
                        sh "terraform get template"
                        sh "terraform plan -var-file=../dev/terraform.tfvars template"
                    }
            }


    }
}

