@Library('sfdi-devops-tools-infra') _

pipeline {
    agent any
    environment{
 	autosys_dev_server= 'emeavopsfa00001'
	autosys_prod_server= 'PRD-AutoSysR12_1'
	jilDirectory='autosys'
	autosys_apiEndpoint='https://amraelp00011107.pfizer.com:9443/AEWS/jil'
	unix_server = "EUZ1PLDW08"
        unix_src_path_scripts = "unix"
        unix_deploy_path_scripts1 = "/app/etl/archival/scripts"
	unix_deploy_path_scripts2 = "/app/etl/archival/parameter_files"
	unix_deploy_path_scripts3 = "/app/etl/palign/ui/emea/scripts"
	unix_deploy_path_scripts4 = "/app/etl/palign/ui/emea/parameter_files"
        unix_deploy_path_scripts5 = "/app/etl/palign/apac/scripts"
	unix_deploy_path_scripts6 = "/app/etl/palign/apac/parameter_files"
	unix_deploy_path_scripts7 = "/app/etl/palign/ui/apac/scripts"
	unix_deploy_path_scripts8 = "/app/etl/palign/ui/apac/parameter_files"
        unix_service_account = "srvamr-palign@amer"
	python_server = "emaaelp00020784" 
        python_src_path_scr = "unix"
        python_src_path_param = "unix"
        python_dest_path_scr = "/app/etl/palign/ui/amer/scripts"
        python_dest_path_param = "/app/etl/palign/ui/amer/parameter_files"
        python_service_account = "srvamr-sfaops" 
        python_group = "unix-palign-u@amer.pfizer.com"
        python_owner = "srvamr-palign@amer.pfizer.com" 
        python_permission = "755"   
	python_priv_key_path = "/var/lib/jenkins/.ssh/id_rsa"   
        unix_permission = "775"
	priv_key_path = "/var/lib/jenkins/.ssh/palign_id_rsa"    
    }
    parameters {
        choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy into Autosys Environment', name: 'Deploy_to_Autosys'
	choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy into Unix Environment', name: 'Deploy_to_Unix'
	choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy into Python', name: 'Deploy_to_Python_Utility'    
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
  
                    	 //sh "ssh -i /var/lib/jenkins/.ssh/palign_id_rsa ${unix_service_account}@${unix_server} 'dzdo chmod 775 ${unix_deploy_path_scripts8}/*'" 
			 //sh "ssh -i /var/lib/jenkins/.ssh/id_rsa srvamr-sfaops@emaaelp00020784 'dzdo chown srvamr-palign@amer.pfizer.com:unix-palign-u@amer.pfizer.com ${unix_deploy_path_scripts8}/*'"
			 sh "scp -i /var/lib/jenkins/.ssh/palign_id_rsa -r ${unix_src_path_scripts}/* ${unix_service_account}@${unix_server}:${unix_deploy_path_scripts1}"
			 sh "ssh -i /var/lib/jenkins/.ssh/palign_id_rsa ${unix_service_account}@${unix_server} 'sudo chmod 775 ${unix_deploy_path_scripts1}/*'"   
			 sh "scp -i /var/lib/jenkins/.ssh/palign_id_rsa -r ${unix_src_path_scripts}/* ${unix_service_account}@${unix_server}:${unix_deploy_path_scripts2}"
			 sh "ssh -i /var/lib/jenkins/.ssh/palign_id_rsa ${unix_service_account}@${unix_server} 'sudo chmod 775 ${unix_deploy_path_scripts2}/*'" 
		    }
                }
        }
        stage ("Deploy to Python"){
            when {
                 expression { params.Deploy_to_Python_Utility == "Yes" }
            }
                steps{
                    script{
			if (params.dry_run == 'Yes') {
        			// Check if dry_run is 'Yes'
        			sh "ls ${python_src_path_scr}"
				sh "ls ${python_src_path_param}"
        			return // Exit the script
    			}
                        sh "scp -i ${env.python_priv_key_path} -r ${env.python_src_path_scr}/* ${env.python_service_account}@${env.python_server}:${env.python_dest_path_scr}"
                        sh "scp -i ${env.python_priv_key_path} -r ${env.python_src_path_param}/* ${env.python_service_account}@${env.python_server}:${env.python_dest_path_param}"
			
			// Set Permissions of the destination files  
			if(python_server == 'emaaelp00020784'){    
				sh "ssh -i ${env.python_priv_key_path} ${env.python_service_account}@${env.python_server} 'dzdo chmod ${env.python_permission} ${env.python_dest_path_scr}/*'"
                        	sh "ssh -i ${env.python_priv_key_path} ${env.python_service_account}@${env.python_server} 'dzdo chmod ${env.python_permission} ${env.python_dest_path_param}/*'"
			}
			else{
				sh "ssh -i ${env.python_priv_key_path} ${env.python_service_account}@${env.python_server} 'sudo chmod ${env.python_permission} ${env.python_dest_path_scr}/*'"
                        	sh "ssh -i ${env.python_priv_key_path} ${env.python_service_account}@${env.python_server} 'sudo chmod ${env.python_permission} ${env.python_dest_path_param}/*'"

			}
                        //Set the owner and file permissions inside a folder
                        if(python_server == 'emaaelp00020784'){
			    sh "ssh -i ${env.python_priv_key_path} ${env.python_service_account}@${env.python_server} 'dzdo chown ${env.python_owner}:${env.python_group} ${env.python_dest_path_scr}/*'"
                            sh "ssh -i ${env.python_priv_key_path} ${env.python_service_account}@${env.python_server} 'dzdo chown ${env.python_owner}:${env.python_group} ${env.python_dest_path_param}/*'"
			}
			else{
			    sh "ssh -i ${env.python_priv_key_path} ${env.python_service_account}@${env.python_server} 'sudo chown ${env.python_owner}:${env.python_group} ${env.python_dest_path_scr}/*'"
                            sh "ssh -i ${env.python_priv_key_path} ${env.python_service_account}@${env.python_server} 'sudo chown ${env.python_owner}:${env.python_group} ${env.python_dest_path_param}/*'"

			}
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
        
    
