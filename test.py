sed -i 's/pa_matillion_master\.ksh PALIGN DEV\(.*\) PFZALGN_DEV PFZALGN_DEV/pa_matillion_master.ksh PALIGN TEST\1 PFZALGN_TEST PFZALGN_TEST/g' "${jilFile}"
