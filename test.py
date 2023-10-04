#!/usr/bin/env groovy

import java.text.SimpleDateFormat
import java.util.Date
import java.util.UUID

def call(Map config) {
    // Your existing code...

    // Function to process JSON data and upload to S3
    def processAndUploadJSON() {
        def requestId = generateRequestID()

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

        // Save JSON data to a file
        def fileToUpload = "${env.WORKSPACE}/output.json"
        writeFile file: fileToUpload, text: jsonString

        // Upload JSON file to S3
        s3Upload(
            consoleLogLevel: 'INFO',
            dontSetBuildResultOnFailure: false,
            dontWaitForConcurrentBuildCompletion: false,
            entries: [
                [bucket: 'mydevopstest', excludedFile: '', flatten: false, gzipFiles: false, keepForever: false,
                    managedArtifacts: false, noUploadOnFailure: false, selectedRegion: 'us-east-1',
                    showDirectlyInBrowser: false, sourceFile: '*json', storageClass: 'STANDARD', uploadFromSlave: false,
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




#!/usr/bin/env groovy
import java.text.SimpleDateFormat
import java.util.Date
import java.util.UUID

def call(Map config) {
    def requestId = generateRequestID()

    // ... (your previous code for generating email content)

    // Generate JSON data
    def jsonParams = [
        "project_name": env.JOB_NAME,
        "branch": env.BRANCH_NAME,
        "project_path": env.WORKSPACE,
        "job_url": env.JOB_DISPLAY_URL,
        "build_id": env.BUILD_ID,
        "build_number": env.BUILD_NUMBER,
        "build_result": currentBuild.result,
        "build_parameters": params,
        "requestid": "${requestId}"
    ]

    // Convert JSON data to string
    def jsonString = groovy.json.JsonOutput.toJson(jsonParams)

    // Save JSON data to a file
    def fileToUpload = "${WORKSPACE}/output.json"
    writeFile file: fileToUpload, text: jsonString

    // Upload file to S3
    s3Upload(
        consoleLogLevel: 'INFO',
        dontSetBuildResultOnFailure: false,
        dontWaitForConcurrentBuildCompletion: false,
        entries: [[
            bucket: 'mydevopstest', // Replace with your actual S3 bucket name
            sourceFile: fileToUpload,
            flatten: true
        ]],
        pluginFailureResultConstraint: 'FAILURE'
    )

    // ... (your previous code for sending email)

    // Rest of your code
}

// Other functions (generateRequestID, formatTimestamp, getParametersTable) remain the same
