#!/usr/bin/env groovy

import java.text.SimpleDateFormat
import java.util.Date
import java.util.UUID

def call(Map config) {
    // Your existing code...

    // Function to process JSON data and upload to S3
    def processAndUploadJSON() {
        def requestId = generateRequestID()

        def projectNameSegments = env.JOB_NAME.split('/')
        def projectName = projectNameSegments[-2] // Assuming the project/pipeline name is the second last segment

        def fileName = "${projectName}_${env.BUILD_NUMBER}_${env.BRANCH_NAME}_${requestId}.json"

        def jsonParams = [
            "project_name": env.JOB_NAME,
            "branch": env.BRANCH_NAME,
            "project_path": env.WORKSPACE,
            "job_url": env.JOB_DISPLAY_URL,
            "build_id": env.BUILD_ID,
            "build_number": env.BUILD_NUMBER,
            "build_result": currentBuild.result,
            "build_parameters": params,
            "requestid": requestId
        ]

        // Convert JSON data to string
        def jsonString = groovy.json.JsonOutput.toJson(jsonParams)

        // Save JSON data to a file with the specified name
        def fileToUpload = "${env.WORKSPACE}/${fileName}"
        writeFile file: fileToUpload, text: jsonString

        // Upload JSON file to S3
        s3Upload(
            consoleLogLevel: 'INFO',
            dontSetBuildResultOnFailure: false,
            dontWaitForConcurrentBuildCompletion: false,
            entries: [
                [bucket: 'mydevopstest', excludedFile: '', flatten: false, gzipFiles: false, keepForever: false,
                    managedArtifacts: false, noUploadOnFailure: false, selectedRegion: 'us-east-1',
                    showDirectlyInBrowser: false, sourceFile: "*${fileName}", storageClass: 'STANDARD', uploadFromSlave: false,
                    useServerSideEncryption: false]
            ],
            pluginFailureResultConstraint: 'FAILURE',
            profileName: 'devops-test',
            userMetadata: []
        )
    }

    if ((env.BRANCH_NAME != 'dev') || (config.Email_Alert == 'Yes')) {
        // Existing code...

        // Call the function to process and upload JSON data
        processAndUploadJSON()

        // More existing code...
    }
    // More existing code...
}

def generateRequestID() {
    // Existing code...
}

def getParametersTable() {
    // Existing code...
}
