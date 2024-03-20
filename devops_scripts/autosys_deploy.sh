#!/bin/bash

failedFiles=() # Array to store failed JIL files
successfulFiles=() # Array to store successful JIL files

USERNAME="${USERNAME}"
PASSWORD="${PASSWORD}"

target_branch=${GIT_BRANCH}
echo "Target branch is: ${target_branch}"
echo "Dry run is: ${dry_run}"
if [ "${dry_run}" = "Yes" ]; then
    echo "Dry run is enabled. Below are the changesets for Autosys deployment:"
    
    # List files in the Autosys folder
    files_in_autosys_folder=$(find "${jilDirectory}" -name '*.jil')
    for file in ${files_in_autosys_folder}; do
        echo "${file}"
    done
    
    # Exit with a successful status
    exit 0
fi

# Get a list of JIL files in the directory
jilFiles=$(find "${jilDirectory}" -name '*.jil')


# Iterate over the JIL files and make POST requests
for jilFile in ${jilFiles}; do
    echo "Processing file: ${jilFile}"
    if [ "${target_branch}" = "test" ]; then
        # Replace string in the JIL file for the "test" branch
        sed -i 's/d2compaemea/t2compaemea/g' "${jilFile}"
        sed -i 's/D2COMPAEMEA/T2COMPAEMEA/g' "${jilFile}"
        sed -i "s/$autosys_dev_server/$autosys_test_server/g" "${jilFile}"
        sed -i 's/pa_postgresql_master.ksh PALIGN DEV/pa_postgresql_master.ksh PALIGN EMEA_TEST/g' "${jilFile}"
        sed -i 's/master_batch_upload.ksh PALIGN DEV/master_batch_upload.ksh PALIGN EMEA_TEST/g' "${jilFile}"
        sed -i 's/master_cascade_notification.ksh DEV/master_cascade_notification.ksh EMEA_TEST/g' "${jilFile}"
        sed -i 's/pa_upload_and_purge_logs.ksh PALIGN DEV/pa_upload_and_purge_logs.ksh PALIGN EMEA_TEST/g' "${jilFile}"
    elif [ "${target_branch}" = "sit" ]; then
        # Replace string in the JIL file for the "sit" branch
        sed -i 's/d2compaemea/s2compaemea/g' "${jilFile}"
        sed -i 's/D2COMPAEMEA/S2COMPAEMEA/g' "${jilFile}"
        sed -i "s/$autosys_dev_server/$autosys_sit_server/g" "${jilFile}"
        sed -i 's/pa_postgresql_master.ksh PALIGN DEV/pa_postgresql_master.ksh PALIGN EMEA_SIT/g' "${jilFile}"
        sed -i 's/master_batch_upload.ksh PALIGN DEV/master_batch_upload.ksh PALIGN EMEA_SIT/g' "${jilFile}"
        sed -i 's/master_cascade_notification.ksh DEV/master_cascade_notification.ksh EMEA_SIT/g' "${jilFile}"
        sed -i 's/pa_upload_and_purge_logs.ksh PALIGN DEV/pa_upload_and_purge_logs.ksh PALIGN EMEA_SIT/g' "${jilFile}"
    elif [ "${target_branch}" = "uat" ]; then
        # Replace string in the JIL file for the "uat" branch
        sed -i 's/d2compaemea/u2compaemea/g' "${jilFile}"
        sed -i 's/D2COMPAEMEA/U2COMPAEMEA/g' "${jilFile}"
        sed -i "s/$autosys_dev_server/$autosys_uat_server/g" "${jilFile}"
        sed -i 's/pa_postgresql_master.ksh PALIGN DEV/pa_postgresql_master.ksh PALIGN EMEA_UAT/g' "${jilFile}"
        sed -i 's/master_batch_upload.ksh PALIGN DEV/master_batch_upload.ksh PALIGN EMEA_UAT/g' "${jilFile}"
        sed -i 's/master_cascade_notification.ksh DEV/master_cascade_notification.ksh EMEA_UAT/g' "${jilFile}"
        sed -i 's/pa_upload_and_purge_logs.ksh PALIGN DEV/pa_upload_and_purge_logs.ksh PALIGN EMEA_UAT/g' "${jilFile}"
    elif [ "${target_branch}" = "master" ]; then
        # Replace string in the JIL file for the "main" branch
        sed -i 's/d2compaemea/p2compaemea/g' "${jilFile}"
        sed -i 's/D2COMPAEMEA/P2COMPAEMEA/g' "${jilFile}"
        sed -i "s/$autosys_dev_server/$autosys_prod_server/g" "${jilFile}"
        sed -i 's/pa_postgresql_master.ksh PALIGN DEV/pa_postgresql_master.ksh PALIGN EMEA_PROD/g' "${jilFile}"
        sed -i 's/master_batch_upload.ksh PALIGN DEV/master_batch_upload.ksh PALIGN EMEA_PROD/g' "${jilFile}"
        sed -i 's/master_cascade_notification.ksh DEV/master_cascade_notification.ksh EMEA_PROD/g' "${jilFile}"
        sed -i 's/pa_upload_and_purge_logs.ksh PALIGN DEV/pa_upload_and_purge_logs.ksh PALIGN EMEA_PROD/g' "${jilFile}"
    fi
    # Perform the curl command
    response=$(curl -X POST -H 'Content-Type: text/plain' --upload-file "${jilFile}" "${autosys_apiEndpoint}" -k --user "${USERNAME}:${PASSWORD}" -i)
    
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
