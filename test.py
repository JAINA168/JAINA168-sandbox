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
