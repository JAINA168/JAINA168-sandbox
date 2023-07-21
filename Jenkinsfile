pipeline {
    agent any
    environment{
 	autosys_main_server= 'amraelp00011108'
	jilDirectory='autosys/'
	apiEndpoint='https://amraelp00011055.pfizer.com:9443/AEWS/jil'
    }
    parameters {
    choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy into Autosys Environment', name: 'Deploy_to_Autosys'
	choice choices: ['No', 'Yes'], description: 'Mention if You want to Deploy into Unix Environment', name: 'Deploy_to_Unix'
       
    }
    stages{
        
        stage ("Deploy to Autosys"){
            when {
                 expression { params.Deploy_to_Autosys == "Yes" }
            }
            steps{		
		//prod server testing		
		        sh 'chmod +x python_scripts/autosys_deploy.sh' 
		        withCredentials([usernamePassword(credentialsId: 'sfaops', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')])
                 {
        		    script {
            			env.PASSWORD = sh(script: "echo \$PASSWORD", returnStdout: true).trim()
            			env.USERNAME = sh(script: "echo \$USERNAME", returnStdout: true).trim()
        		    } 	
			    sh 'python_scripts/autosys_deploy.sh'			
		        }
		}
	}
	 stage ("Deploy to Unix"){
            when {
                 expression { params.Deploy_to_Unix == "Yes" }
            }
                steps{
                    script{
        sh "scp -i /var/lib/jenkins/.ssh/id_rsa test1.py srvamr-sfaops@amer@EUZ1PLDW08:/app/etl/repl/scripts"
		sh "ssh -i /var/lib/jenkins/.ssh/id_rsa srvamr-sfaops@amer@EUZ1PLDW08 'sudo chmod 775 /app/etl/repl/scripts/*'"
		
		    }
                }
        }
            
				
        }
    }
