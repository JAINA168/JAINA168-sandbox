@Library('sfdi-devops-tools-infra') _

pipeline {
    agent any
    environment{
 	autosys_dev_server= 'emeavopsfa00001'
	autosys_prod_server= 'PRD-AutoSysR12_1'
	jilDirectory='autosys'
	autosys_apiEndpoint='https://amraelp00011107.pfizer.com:9443/AEWS/jil'
	unix_server = "emaaelp00020784"
        unix_src_path_scripts = "unix"
        unix_deploy_path_scripts1 = "/app/etl/palign/emea/scripts"
	unix_deploy_path_scripts2 = "/app/etl/palign/emea/parameter_files"
	unix_deploy_path_scripts3 = "/app/etl/palign/ui/emea/scripts"
	unix_deploy_path_scripts4 = "/app/etl/palign/ui/emea/parameter_files"
        unix_service_account = "srvamr-sfaops"
        unix_permission = "775"
	priv_key_path = "/var/lib/jenkins/.ssh/palign_id_rsa"    
    }
    parameters {
        choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy into Autosys Environment', name: 'Deploy_to_Autosys'
	choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy into Unix Environment', name: 'Deploy_to_Unix'
	choice choices: ['Yes', 'No'], description: 'Mention if You want to Dry Run', name: 'dry_run'    
	choice choices: ['No', 'Yes'], description: 'If you want to send alerts', name: 'Email_Alert'
        string defaultValue: 'None', description: 'Provide the comma separated Email addresses.', name: 'Notify_to'
       
    }
    stages{
        stage ("Deploy to Unix"){
            when {
                 expression { params.Deploy_to_Unix == "Yes" }
            }
                steps{
                    script{
                        if (params.dry_run == 'Yes') {
        			// Check if dry_run is 'Yes'
        			sh "ls ${unix_src_path_scripts}"
        			return // Exit the script
    			}
			     sh "echo test successful"
			 sh "scp -i /var/lib/jenkins/.ssh/id_rsa -r ${unix_src_path_scripts}/* ${unix_service_account}@${unix_server}:${unix_deploy_path_scripts1}"    
                    	 sh "ssh -i /var/lib/jenkins/.ssh/id_rsa ${unix_service_account}@${unix_server} 'chmod 775 ${unix_deploy_path_scripts1}/*'" 
			 sh "scp -i /var/lib/jenkins/.ssh/id_rsa -r ${unix_src_path_scripts}/* ${unix_service_account}@${unix_server}:${unix_deploy_path_scripts2}"    
                    	 sh "ssh -i /var/lib/jenkins/.ssh/id_rsa ${unix_service_account}@${unix_server} 'chmod 775 ${unix_deploy_path_scripts2}/*'" 
			 sh "scp -i /var/lib/jenkins/.ssh/id_rsa -r ${unix_src_path_scripts}/* ${unix_service_account}@${unix_server}:${unix_deploy_path_scripts3}"    
                    	 sh "ssh -i /var/lib/jenkins/.ssh/id_rsa ${unix_service_account}@${unix_server} 'chmod 775 ${unix_deploy_path_scripts3}/*'" 
			 sh "scp -i /var/lib/jenkins/.ssh/id_rsa -r ${unix_src_path_scripts}/* ${unix_service_account}@${unix_server}:${unix_deploy_path_scripts4}"    
                    	 sh "ssh -i /var/lib/jenkins/.ssh/id_rsa ${unix_service_account}@${unix_server} 'chmod 775 ${unix_deploy_path_scripts4}/*'" 
		    }
                }
        }
        
         stage ("Deploy to Autosys"){
            when {
                 expression { params.Deploy_to_Autosys == "Yes" }
            }
            steps{
                script{
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
        
    
