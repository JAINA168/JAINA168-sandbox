@Library('sfdi-devops-tools-infra') _

pipeline {
    agent any
    environment {
        pgdb_credid = "${env.BRANCH_NAME}_pgdb_credid_ui"
        pgdb_url = "${getProperty("${env.BRANCH_NAME}_pfzalgn_pgdb_url")}"
        pgdb_changeLogFile = "Backend/publish/postgres/changelog.pg.xml"
        unix_server = "${getProperty("${env.BRANCH_NAME}_pfzalgn_unix_server_publish")}"
        // unix source paths for publish
        unix_scripts_path = "Backend/publish/unix/scripts"
        unix_config = "Backend/publish/unix/config_files"
        // unix_arc_process_path = "Backend/publish/unix/archive_processed"
        // unix_arc_raw_path = "Backend/publish/unix/archive_raw"
        // unix_inb_raw_path = "Backend/publish/unix/inbound_raw"
        // unix_inb_error_path = "Backend/publish/unix/inbound_error"
        // unix_inb_process_path = "Backend/publish/unix/inbound_processed"
        // unix_logs_path = "Backend/publish/unix/logs"
        // unix deploy paths for publish
        unix_deploy_path_scripts = "/app/etl/palign/scripts"
        unix_deploy_path_config = "/home/srvamr-palign/.snowsql"
        // unix_deploy_path_arc_process = "/app/etl/palign/archive/processed"
        // unix_deploy_path_arc_raw = "/app/etl/palign/archive/raw"
        // unix_deploy_path_inb_raw = "/app/etl/palign/inbound/raw"
        // unix_deploy_path_inb_error = "/app/etl/palign/inbound/error"
        // unix_deploy_path_inb_process = "/app/etl/palign/inbound/processed"
        // unix_deploy_path_logs = "/app/etl/palign/archive/raw"
        unix_service_account = "srvamr-palign@amer"
        snowflake_changeLogFile_COMETL_CONTROL__db = "Backend/publish/snowflake/COMETL_CONTROL/changelog.sf.xml"
        snowflake_changeLogFile_COMETL_PA__db = "Backend/publish/snowflake/COMETL_PA_ODS/changelog.sf.xml"
        snowflake_COMETL_CONTROL__db_url = "${getProperty("${env.BRANCH_NAME}_pfzalgn_snowflake_COMETL_CONTROL_db_url_publish")}"
        snowflake_COMETL_PA__db_url = "${getProperty("${env.BRANCH_NAME}_pfzalgn_snowflake_COMETL_PA_ODS_db_url_publish")}"
        snowflake_credid = "${env.BRANCH_NAME}_pfzalgn_snowflake_credid"
        unix_permission = "775"
	jilDirectory= 'Backend/publish/autosys'
        autosys_apiEndpoint= "${getProperty("${env.BRANCH_NAME}_autosys_apiEndpoint")}"
        autosys_dev_server= 'amrvopsfa000001'
        autosys_test_server='amrvotpa000001'
        autosys_sit_server= 'amrvoupa000001'
        autosys_uat_server= 'amrvospa000002'
        autosys_prod_server= "${getProperty("${env.BRANCH_NAME}_autosys_server")}"  
    }
    parameters {
        choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy into PostgreSQL Environment', name: 'Deploy_to_PostgreSQL'
        choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy into Unix Environment', name: 'Deploy_to_Unix'
        choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy into Snowflake Environment', name: 'Deploy_to_Snowflake_COMETL_CONTROL'
        choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy into Snowflake Environment', name: 'Deploy_to_Snowflake_COMETL_PA'
        choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy Autosys', name: 'Deploy_to_Autosys'
        choice choices: ['Yes', 'No'], description: 'Mention if You want to Dry Run', name: 'dry_run'
        choice choices: ['No', 'Yes'], description: 'If you want to send alerts', name: 'Email_Alert'
        string defaultValue: 'None', description: 'Provide the comma separated Email addresses.', name: 'Notify_to'
    }
    stages{
        stage("Approval for Prod"){
            when {
                expression { "${env.BRANCH_NAME}" == "main" }
            }
            steps{
                script{
                    email_approval()
                }
            }
        }
        stage ("Deploy to PostgreSQL"){
            when {
                 expression { params.Deploy_to_PostgreSQL == "Yes" }
            }
            steps{
                script{
                        sh """
                            cd Backend/grw/postgres
                            ls
                        """
                        postgresql_deploy(url: pgdb_url, cred: pgdb_credid, changelog: pgdb_changeLogFile, dry_run: dry_run)
                    }
                }
        }
        stage ("Deploy to Unix"){
            when {
                 expression { params.Deploy_to_Unix == "Yes" }
            }
                steps{
                    script{
                        sh "echo test successful"
                        // unix_deploy(src: unix_scripts_path, dest: unix_deploy_path_scripts, server: unix_server, service_account: unix_service_account, permissions: unix_permission, dry_run: dry_run)
                        // unix_deploy(src: unix_config, dest: unix_deploy_path_config, server: unix_server, service_account: unix_service_account, permissions: unix_permission, dry_run: dry_run)
                        }
                }
        }
        stage ("Deploy to Autosys"){
            when {
                 expression { params.Deploy_to_Autosys == "Yes" }
            }
            steps{		
		        sh 'chmod +x devops_scripts/autosys_deploy.sh' 
		        withCredentials([usernamePassword(credentialsId: 'sfaops', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
        		    script {
            			env.PASSWORD = sh(script: "echo \$PASSWORD", returnStdout: true).trim()
            			env.USERNAME = sh(script: "echo \$USERNAME", returnStdout: true).trim()
        		    } 	
			    sh 'devops_scripts/autosys_deploy.sh'			
		        }
            }		
        }
    }
    post {
        failure {
            notification_email(Email_Alert: Email_Alert, Notify_to: Notify_to) 
        }
        success {
            notification_email(Email_Alert: Email_Alert, Notify_to: Notify_to)
        }
    }
}
