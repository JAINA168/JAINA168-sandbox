#!/usr/bin/env groovy

def call(Map config) {
    // Your existing code...

    // Function to upload log file to S3 with custom file name
    def uploadLogToS3() {
        def s3Bucket = 'mydevopstest'
        def s3Path = 'build-logs/'

        def projectNameSegments = currentBuild.fullProjectName.split('/')
        def sfa = projectNameSegments[-3]
        def Pfizer_Align_UI = projectNameSegments[-2]
        def branch = projectNameSegments[-1]

        def job_split = "jobs/${sfa}/jobs/${Pfizer_Align_UI}/branches/${branch}/builds"
        def final_job = "${JENKINS_HOME}/${job_split}/${BUILD_NUMBER}/log"
        
        def newFileName = "${sfa}_${Pfizer_Align_UI}_${BUILD_NUMBER}_${branch}_DeploymentReqNum.txt"

        // Echo the job URL and log file path
        echo "Job URL: ${job_split}"
        echo "Log File Path: ${final_job}"
        echo "Workspace: ${WORKSPACE}"

        // Rename log file to custom name
        sh "mv ${final_job} ${WORKSPACE}/${newFileName}"

        // Upload renamed log file to S3
        s3Upload consoleLogLevel: 'INFO', dontSetBuildResultOnFailure: false,
                dontWaitForConcurrentBuildCompletion: false,
                entries: [[bucket: s3Bucket, excludedFile: '', flatten: false,
                gzipFiles: false, keepForever: false, managedArtifacts: false,
                noUploadOnFailure: false, selectedRegion: 'us-east-1',
                showDirectlyInBrowser: false, sourceFile: newFileName,
                storageClass: 'STANDARD', uploadFromSlave: false,
                useServerSideEncryption: false]],
                pluginFailureResultConstraint: 'FAILURE',
                profileName: 'devops-test', userMetadata: []
    }

    // Call the function within the script map
    uploadLogToS3()

    // Your existing code...
}
