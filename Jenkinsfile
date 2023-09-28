@Library('sfdi-devops-tools-infra') _
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
			   sh '''         echo "This is a multiline script"         echo "You can run multiple Unix commands here"         ls -l     '''
                 //sh "scp -i /var/lib/jenkins/.ssh/id_rsa -r test1.py srvamr-sfaops@amer@EUZ1PLDW08:/app/etl/repl/scripts"
		// sh "ssh -i /var/lib/jenkins/.ssh/id_rsa srvamr-sfaops@amer@EUZ1PLDW08 'sudo chmod 775 /app/etl/repl/scripts/*'"
		
		    }
                }
        }
            
				
        }
	post {
        always {
            script {
                 def s3Bucket = 'mydevopstest'
                    def s3Path = 'build-logs/'
                    sh 'touch demo.txt'
                    sh 'echo $JOB_NAME'
                    sh 'echo $JOB_BASE_NAME'
                    sh 'echo $JENKINS_HOME'

                   def projectNameSegments = currentBuild.fullProjectName.split('/')
                    echo "${projectNameSegments}"

                    def sfa = projectNameSegments[-3]
                    def Pfizer_Align_UI = projectNameSegments[-2]
                    def branch = projectNameSegments[-1]

                    def job_split = "jobs/${sfa}/jobs/${Pfizer_Align_UI}/branches/${branch}/builds"
                    def final_job = "${JENKINS_HOME}/${job_split}/${BUILD_NUMBER}/log"
 

                    sh "echo Job URL: ${job_split}"
                    sh "echo Job URL: ${final_job}"
                    sh "echo ${WORKSPACE}"
                    sh "cp ${final_job} ${WORKSPACE}"
		    s3Upload consoleLogLevel: 'INFO', dontSetBuildResultOnFailure: false, dontWaitForConcurrentBuildCompletion: false, entries: [[bucket: 'mydevopstest', excludedFile: '', flatten: false, gzipFiles: false, keepForever: false, managedArtifacts: false, noUploadOnFailure: false, selectedRegion: 'us-east-1', showDirectlyInBrowser: false, sourceFile: 'log', storageClass: 'STANDARD', uploadFromSlave: false, useServerSideEncryption: false]], pluginFailureResultConstraint: 'FAILURE', profileName: 'devops-test', userMetadata: []


 

                // Archive the build log
                archiveArtifacts artifacts: '${BUILD_URL}/consoleText', allowEmptyArchive: true

 

                // Publish the build log to S3
                s3Upload(credentialsId: 'S3Credentials', 
                         bucket: s3Bucket, 
                         sourceFile: '${BUILD_URL}/consoleText', 
                         target: s3Path + env.BRANCH_NAME + '/build-${BUILD_NUMBER}.log')
            }
        }
    }
    }
