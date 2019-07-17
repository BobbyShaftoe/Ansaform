@Library("PipelineLibrary") _

env.JOB_NODE_NAME = 'aws-node-00'


node('aws-node-00') {
    ansiColor('xterm') {

        WORKSPACE = pwd()

        stage('Set default workspace and cleanup') {
            echo "WORKSPACE"
            echo "${WORKSPACE}"
            sh 'rm -rf ${WORKSPACE}/*'
        }

        stage('Setup Check') {
            setupCheck {}
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


        stage('Checkout ansible repo') {
            checkoutRepo('https://github.com/BobbyShaftoe/Ansaform.git', WORKSPACE)
        }

        stage('Download Terraform') {
            def terraform_binary = '${WORKSPACE}/Ansaform/terraform'
            def terraform_zip = '${WORKSPACE}/Ansaform/terraform.zip'
            sh "curl https://releases.hashicorp.com/terraform/0.12.4/terraform_0.12.4_linux_amd64.zip -o " + terraform_zip

            sh "unzip " + terraform_zip + " -d " + '${WORKSPACE}/Ansaform'
            sh "chmod ugo+x " + terraform_binary
            sh "ls -la *"
        }

        stage("Terraform plan") {
            def ansaform_dir = WORKSPACE + '/Ansaform'
            dir("$ansaform_dir") {
                sh "pwd"
                sh "ls -la"
                sh "file terraform"
                sh "./terraform init template"
                sh "./terraform get template"
                sh "./terraform refresh -var-file=../dev/terraform.tfvars template"
                sh "./terraform plan -var-file=../dev/terraform.tfvars template"
                sh "./terraform apply -auto-approve -var-file=../dev/terraform.tfvars template"


                def config_dir = WORKSPACE + '/Ansaform'
                dir("$config_dir") {
                    sh "../terraform state pull > template/terraform.tfstate"
                }

                sh "ls -la " + ansaform_dir
            }
        }

        stage('Ansaform'){
            def terraform_statefile_path = WORKSPACE + '/Ansaform/template/terraform.tfstate'
            def ansible_dir = WORKSPACE + '/Ansaform/ansible'
            dir("$ansible_dir"){
                sh "ansible-playbook -i hosts.ini --extra-vars " +
                        "terraform_statefile_path='${terraform_statefile_path}' terraform-testing.yml"
            }

        }

        stage('Collate all'){
            def terraform_statefile_path = WORKSPACE + '/Ansaform/template/terraform.tfstate'
            def ansible_dir = WORKSPACE + '/Ansaform/ansible'
            def ansaform_reports_dir = WORKSPACE + '/Ansaform/ansible/tests'
            def junit2html_dir = WORKSPACE + '/Ansaform/lib/junit2html'
            def ansaform_dir = WORKSPACE + '/Ansaform'
            def documentation_dir = WORKSPACE + '/Ansaform/documentation'

            sh ". /opt/virtualenv/py36/bin/activate"

            dir("$ansaform_reports_dir"){
                sh "python " + junit2html_dir + "/junit2html.py -m aws-resource-attributes-test-report.xml *"
            }

        }

        stage('build documentation') {
            def documentation_dir = WORKSPACE + '/Ansaform/documentation'
            sh ". /opt/virtualenv/py36/bin/activate"
            dir("$documentation_dir") {
                sh "make html"
            }
        }





    }
}












//node('aws-node-00') {
//    ansiColor('xterm') {
//        environment {
//            JOB_DEFINITION = 'Test'
//        }
//
//            stage('Set default workspace') {
//                echo env.WORKSPACE
//
//            }
//
//            stage('Retrieve scm vars') {
//                def checkoutVars = checkout scm
//                def commit_id = checkoutVars.GIT_COMMIT
//                env.GIT_COMMIT = checkoutVars.GIT_COMMIT
//                env.GIT_BRANCH = checkoutVars.GIT_BRANCH
//                env.GIT_LOCAL_BRANCH = checkoutVars.GIT_LOCAL_BRANCH
//                env.GIT_PREVIOUS_COMMIT = checkoutVars.GIT_PREVIOUS_COMMIT
//                env.GIT_URL = checkoutVars.GIT_URL
//            }
//
//            stage('Checkout scm') {
//                checkout scm
//            }
//
//            stage('Checkout ansible repo') {
//                checkoutRepo('https://github.com/BobbyShaftoe/Ansaform.git')
//            }
//
//            stage('Download Terraform') {
//
//                    def out='$(pwd)/Ansaform/terraform'
//                    sh "curl https://releases.hashicorp.com/terraform/0.12.4/terraform_0.12.4_linux_amd64.zip -o " + out
//                    sh "chmod ugo+x " + out
//                    sh "ls -la *"
//
//            }
//
//            stage('Setup Check') {
//                setupCheck {}
//            }
//
//            stage("Terraform plan") {
//                def ansaform_dir='$(pwd)/Ansaform'
//                dir(ansaform_dir) {
//                    sh "pwd"
//                    sh "ls -la"
//
//                    sh "terraform init template"
//                    sh "terraform get template"
//                    sh "terraform plan -var-file=../dev/terraform.tfvars template"
//                }
//            }
//
//
//    }
//}

