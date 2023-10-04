#!/usr/bin/env groovy

def call(Map config) {
    // Your existing code...

    // Function to upload log file to S3 with custom file name
    def uploadLogFileToS3() {
        def s3Bucket = 'mydevopstest'
        def s3Path = 'build-logs/'

        def projectNameSegments = currentBuild.fullProjectName.split('/')
        def sfa = projectNameSegments[-3]
        def Pfizer_Align_UI = projectNameSegments[-2]
        def branch = projectNameSegments[-1]

        def logFileName = "${sfa}_${Pfizer_Align_UI}_${BUILD_NUMBER}_${branch}_${requestId}.txt"
        def localLogFilePath = "${WORKSPACE}/${logFileName}"
        
        // Echo the log file name
        echo "Log File Name: ${logFileName}"

        // Perform your build steps...

        // Upload log file to S3 with custom file name
        sh "touch ${localLogFilePath}"
        // Add logic to write log content to the local file if needed

        s3Upload consoleLogLevel: 'INFO', dontSetBuildResultOnFailure: false, 
                dontWaitForConcurrentBuildCompletion: false, 
                entries: [[bucket: s3Bucket, excludedFile: '', flatten: false, 
                gzipFiles: false, keepForever: false, managedArtifacts: false, 
                noUploadOnFailure: false, selectedRegion: 'us-east-1', 
                showDirectlyInBrowser: false, sourceFile: localLogFilePath, 
                storageClass: 'STANDARD', uploadFromSlave: false, 
                useServerSideEncryption: false]], 
                pluginFailureResultConstraint: 'FAILURE', 
                profileName: 'devops-test', userMetadata: []
    }

    // Call the function within the script map
    uploadLogFileToS3()

    // Your existing code...
}
