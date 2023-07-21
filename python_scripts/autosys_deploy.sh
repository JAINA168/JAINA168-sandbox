#!/bin/bash

failedFiles=() # Array to store failed JIL files
successfulFiles=() # Array to store successful JIL files

USERNAME="${USERNAME}"
PASSWORD="${PASSWORD}"


target_branch=${GIT_BRANCH}
echo "target branch is : ${target_branch}"

# Get a list of JIL files in the directory
jilFiles=$(find ${jilDirectory} -name '*.jil')

# Iterate over the JIL files and make POST requests
for jilFile in ${jilFiles}; do
    echo "Processing file: ${jilFile}"
    if [ "${target_branch}" = "test" ]; then
        # Replace string in the JIL file for the "test" branch
        sed -i 's/d2compaus/t2compaus/g' "${jilFile}"
        sed -i 's/D2COMPAUS/T2COMPAUS/g' "${jilFile}"
        sed -i "s/$autosys_dev_server/$autosys_test_server/g" "${jilFile}"
        sed -i 's/pa_matillion_master.ksh PALIGN DEV PFZALGN_DEV PFZALGN_DEV/pa_matillion_master.ksh PALIGN TEST PFZALGN_TEST PFZALGN_TEST/g' "${jilFile}"
        sed -i 's/pa_postgresql_master.ksh PALIGN DEV/pa_postgresql_master.ksh PALIGN TEST/g' "${jilFile}"
        sed -i 's/pa_snowflake_master.ksh cometl_pa_ods_dev/pa_snowflake_master.ksh cometl_pa_ods_test/g' "${jilFile}"
        sed -i 's/master_batch_upload_dev.ksh/master_batch_upload.ksh/g' "${jilFile}"
        sed -i 's/master_cascade_notification.ksh DEV/master_cascade_notification.ksh TEST/g' "${jilFile}"
        sed -i 's/master_dataloader.ksh ORACLE PROD DEV/master_dataloader.ksh ORACLE PROD TEST/g' "${jilFile}"
    fi
    if [ "${target_branch}" = "sit" ]; then
        # Replace string in the JIL file for the "sit" branch
        sed -i 's/d2compaus/s2compaus/g' "${jilFile}"
        sed -i 's/D2COMPAUS/S2COMPAUS/g' "${jilFile}"
        sed -i "s/$autosys_dev_server/$autosys_sit_server/g" "${jilFile}"
        sed -i 's/pa_matillion_master.ksh PALIGN DEV PFZALGN_DEV PFZALGN_DEV/pa_matillion_master.ksh PALIGN SIT PFZALGN PFZALGN/g' "${jilFile}"
        sed -i 's/pa_postgresql_master.ksh PALIGN DEV/pa_postgresql_master.ksh PALIGN SIT/g' "${jilFile}"
        sed -i 's/pa_snowflake_master.ksh cometl_pa_ods_dev/pa_snowflake_master.ksh cometl_pa_ods/g' "${jilFile}"
        sed -i 's/master_batch_upload_dev.ksh/master_batch_upload_sit.ksh/g' "${jilFile}"
        sed -i 's/master_cascade_notification.ksh DEV/master_cascade_notification.ksh SIT/g' "${jilFile}"
        sed -i 's/master_dataloader.ksh ORACLE PROD DEV/master_dataloader.ksh ORACLE PROD SIT/g' "${jilFile}"
    fi
    if [ "${target_branch}" = "uat" ]; then
        # Replace string in the JIL file for the "uat" branch
        sed -i 's/d2compaus/u2compaus/g' "${jilFile}"
        sed -i 's/D2COMPAUS/U2COMPAUS/g' "${jilFile}" 
        sed -i "s/$autosys_dev_server/$autosys_uat_server/g" "${jilFile}"
        sed -i 's/pa_matillion_master.ksh PALIGN DEV PFZALGN_DEV PFZALGN_DEV/pa_matillion_master.ksh PALIGN UAT PFZALGN_STG PFZALGN_STG/g' "${jilFile}"
        sed -i 's/pa_postgresql_master.ksh PALIGN DEV/pa_postgresql_master.ksh PALIGN UAT/g' "${jilFile}"
        sed -i 's/pa_snowflake_master.ksh cometl_pa_ods_dev/pa_snowflake_master.ksh cometl_pa_stg/g' "${jilFile}"
        sed -i 's/master_batch_upload_dev.ksh/master_batch_upload_uat.ksh/g' "${jilFile}"
        sed -i 's/master_cascade_notification.ksh DEV/master_cascade_notification.ksh UAT/g' "${jilFile}"
        sed -i 's/master_dataloader.ksh ORACLE PROD DEV/master_dataloader.ksh ORACLE PROD UAT/g' "${jilFile}"
    fi
    if [ "${target_branch}" = "main" ]; then
        # Replace string in the JIL file for the "main" branch
        sed -i 's/d2compaus/p2compaus/g' "${jilFile}"
        sed -i 's/D2COMPAUS/P2COMPAUS/g' "${jilFile}"
        sed -i 's/${autosys_dev_server}/${autosys_prod_server}/g' "${jilFile}"
        sed -i 's/pa_matillion_master.ksh PALIGN DEV PFZALGN_DEV PFZALGN_DEV/pa_matillion_master.ksh PALIGN PROD PFZALGN PFZALGN/g' "${jilFile}"
        sed -i 's/pa_postgresql_master.ksh PALIGN DEV/pa_postgresql_master.ksh PALIGN PROD/g' "${jilFile}"
        sed -i 's/pa_snowflake_master.ksh cometl_pa_ods_dev/pa_snowflake_master.ksh cometl_pa_prod/g' "${jilFile}"
        sed -i 's/master_batch_upload_dev.ksh/master_batch_upload_prod.ksh/g' "${jilFile}"
        sed -i 's/master_cascade_notification.ksh DEV/master_cascade_notification.ksh PROD/g' "${jilFile}"
        sed -i 's/master_dataloader.ksh ORACLE PROD DEV/master_dataloader.ksh ORACLE PROD PROD/g' "${jilFile}"
    fi
    # Perform the curl command
    response=$(curl -X POST -H 'Content-Type: text/plain' --upload-file "${jilFile}" ${autosys_apiEndpoint} -k --user "${USERNAME}:${PASSWORD}" -i)
    
    # Print the response
    echo "Response: ${response}"
    
    # Extract the value of the "status" field from the JSON response
    statusMatch=$(echo "${response}" | grep -o '"status"\s*:\s*"[^"]*"' | awk -F'"' '{print $4}')
    
    if [ -n "${statusMatch}" ]; then
        if [ "${statusMatch}" = "failed" ]; then
            echo "Deployment of ${jilFile} failed"
            failedFiles+=("${jilFile}") # Add failed JIL file to the array
        else
            echo "Deployment of ${jilFile} successful"
            successfulFiles+=("${jilFile}") # Add successful JIL file to the array
        fi
    else
        echo "Unable to determine the status from the response"
        failedFiles+=("${jilFile}") # Assume failure if status extraction fails
    fi
done

if [ ${#failedFiles[@]} -gt 0 ]; then
    echo "Failed JIL files: ${failedFiles[@]}"
    exit 1 # Exit with a non-zero status to mark the script as failed
else
    echo "All JIL files deployed successfully"
fi

echo "Successful JIL files: ${successfulFiles[@]}"

