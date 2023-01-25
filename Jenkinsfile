@Library('library-demo') _

pipeline {
    agent any
    parameters {
        string defaultValue: '_DEV_', name: 'source_string', trim: true
        string defaultValue: '_TEST_', name: 'replacement_string', trim: true
    }
    stages{
         stage("Replacement String"){
            steps{
                script{
                   sh '''
                        ls
                        cat test1.sql
                        cat test2.sql
                        find . -type f -name "*.sql" -print0 | xargs -0 sed -i "s/$source_string/$replacement_string/g"
                        cat test1.sql
                        cat test2.sql
                   ''' 
        }
    }
}

    }}