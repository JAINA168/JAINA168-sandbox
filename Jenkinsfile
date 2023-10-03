@Library('sfdi-devops-tools-infra') _

pipeline {
    agent any
    environment{
 	autosys_main_server= 'amraelp00011593'
	jilDirectory='autosys/'
	autosys_apiEndpoint='https://amraelp00011055.pfizer.com:9443/AEWS/jil'
	unix_server = "amrvopsfa000001"
        unix_src_path_scripts = "autosys"
        unix_deploy_path_scripts = "/tmp"
        unix_service_account = "srvamr-palign@amer"
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
			sh "scp -i ${priv_key_path} -r ${unix_src_path_scripts}/* ${unix_service_account}@${unix_server}:${unix_deploy_path_scripts}"    
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
			    sh "devops_scripts/autosys_deploy.sh" // Pass the params			
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
        
    
