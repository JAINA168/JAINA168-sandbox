|| PODNAME || Unix || PostgressSQL || Snowflake ||
| Dev | Test | SIT | UAT | Prod | Dev | Test | SIT | UAT | Prod | Dev | Test | SIT | UAT | Prod |
| Data conversion | EMEAVOPSFA00001 | "EMAAELP00010092 IP: 10.90.82.109" | NA | NA | NA | jdbc:postgresql://pfzalgn-emea-dev.cmp0gpuhg8ox.eu-west-1.rds.amazonaws.com:5432/PFZALGEMEATD | "EMEA:jdbc:postgresql://pfzalgn-emea-test.cluster-cmp0gpuhg8ox.eu-west-1.rds.amazonaws.com:5432/PFZALGEMEATT APAC:jdbc:postgresql://pfzalgn-apac-test.cluster-cmp0gpuhg8ox.eu-west-1.rds.amazonaws.com:5432/PFZALGAPACTT" | NA | NA | NA | "Control-jdbc:snowflake://emeadev01.eu-west-1.privatelink.snowflakecomputing.com/ ?role=COMETL_PA_EMEA_DEV_RW_ROLE&warehouse=COMETL_PA_EMEA_DEV_XSMALL_WH&db=COMETL_CONTROL_DEV_DB&schema=COMETL_CONTROL&multi_statement_count=0 Control-jdbc:snowflake://emeadev01.eu-west-1.privatelink.snowflakecomputing.com/ ?role=COMETL_PA_EMEA_DEV_RW_ROLE&warehouse=COMETL_PA_EMEA_DEV_XSMALL_WH&db=COMETL_PA_EMEA_DEV_DB&schema=COMETL_PA_INT_STG&multi_statement_count=0 jdbc:snowflake://emeadev01.eu-west-1.privatelink.snowflakecomputing.com/ ?role=COMETL_PA_APAC_TEST_RW_ROLE&warehouse=COMETL_PA_APAC_TEST_XSMALL_WH&db=COMETL_PA_APAC_TEST_DB&schema=COMETL_PA_INT_STG&multi_statement_count=0" | NA | NA |






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
