provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "aws_service_role_for_amazon_connect" {
  name = "AWSServiceRoleForAmazonConnect_N9FSnJSLAy3Hjpeixw5h"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "connect.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })

  max_session_duration = 3600
}

data "aws_iam_policy_document" "amazon_connect_service_data_stream_agent_events" {
  policy = file("policies/AmazonConnectServiceDataStreamAgentEvents.json")
}

resource "aws_iam_policy" "amazon_connect_service_data_stream_agent_events" {
  name   = "AmazonConnectServiceDataStreamAgentEvents"
  policy = data.aws_iam_policy_document.amazon_connect_service_data_stream_agent_events.json
}

data "aws_iam_policy_document" "amazon_connect_service_data_stream_contact_trace_record" {
  policy = file("policies/AmazonConnectServiceDataStreamContactTraceRecord.json")
}

resource "aws_iam_policy" "amazon_connect_service_data_stream_contact_trace_record" {
  name   = "AmazonConnectServiceDataStreamContactTraceRecord"
  policy = data.aws_iam_policy_document.amazon_connect_service_data_stream_contact_trace_record.json
}

data "aws_iam_policy_document" "amazon_connect_service_linked_role_policy" {
  policy = file("policies/AmazonConnectServiceLinkedRolePolicy.json")
}

resource "aws_iam_policy" "amazon_connect_service_linked_role_policy" {
  name   = "AmazonConnectServiceLinkedRolePolicy"
  policy = data.aws_iam_policy_document.amazon_connect_service_linked_role_policy.json
}

data "aws_iam_policy_document" "amazon_connect_service_live_media_streaming_access" {
  policy = file("policies/AmazonConnectServiceLiveMediaStreamingAccess.json")
}

resource "aws_iam_policy" "amazon_connect_service_live_media_streaming_access" {
  name   = "AmazonConnectServiceLiveMediaStreamingAccess"
  policy = data.aws_iam_policy_document.amazon_connect_service_live_media_streaming_access.json
}

resource "aws_iam_role_policy_attachment" "attach_data_stream_agent_events_policy" {
  role       = aws_iam_role.aws_service_role_for_amazon_connect.name
  policy_arn = aws_iam_policy.amazon_connect_service_data_stream_agent_events.arn
}

resource "aws_iam_role_policy_attachment" "attach_data_stream_contact_trace_record_policy" {
  role       = aws_iam_role.aws_service_role_for_amazon_connect.name
  policy_arn = aws_iam_policy.amazon_connect_service_data_stream_contact_trace_record.arn
}

resource "aws_iam_role_policy_attachment" "attach_service_linked_role_policy" {
  role       = aws_iam_role.aws_service_role_for_amazon_connect.name
  policy_arn = aws_iam_policy.amazon_connect_service_linked_role_policy.arn
}

resource "aws_iam_role_policy_attachment" "attach_live_media_streaming_access_policy" {
  role       = aws_iam_role.aws_service_role_for_amazon_connect.name
  policy_arn = aws_iam_policy.amazon_connect_service_live_media_streaming_access.arn
}
To avoid using the `data` module, you can directly reference the JSON files using the `file` function. Here’s how you can update your Terraform configuration to do so:

1. **Create the `policy` Folder and JSON Policy Files**:
   Ensure you have a folder named `policy` and save your IAM policies in separate JSON files inside this folder.

   - **policy/lambda_assume_role_policy.json**:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Principal": {
             "Service": "lambda.amazonaws.com"
           },
           "Action": "sts:AssumeRole"
         }
       ]
     }
     ```

   - **policy/lambda_policy.json**:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": [
             "logs:CreateLogGroup",
             "logs:CreateLogStream",
             "logs:PutLogEvents"
           ],
           "Resource": "arn:aws:logs:*:*:*"
         },
         {
           "Effect": "Allow",
           "Action": "lambda:InvokeFunction",
           "Resource": "*"
         },
         {
           "Effect": "Allow",
           "Action": [
             "kinesisvideo:*"
           ],
           "Resource": "arn:aws:kinesisvideo:ap-northeast-1:864033247427:*"
         }
       ]
     }
     ```

2. **Terraform Configuration**:
   Reference the JSON policy files directly in your Terraform configuration.

   - **main.tf**:
     ```hcl
     provider "aws" {
       region = "ap-northeast-1"
     }

     resource "aws_iam_role" "lambda_role" {
       name = "lambda_role"

       assume_role_policy = file("policy/lambda_assume_role_policy.json")
     }

     resource "aws_iam_policy" "lambda_policy" {
       name        = "lambda_policy"
       description = "IAM policy for Lambda functions"
       policy      = file("policy/lambda_policy.json")
     }

     resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
       role       = aws_iam_role.lambda_role.name
       policy_arn = aws_iam_policy.lambda_policy.arn
     }

     resource "aws_lambda_function" "connect_lambda" {
       function_name = "ConnectLambdaFunction"
       role          = aws_iam_role.lambda_role.arn
       handler       = "index.handler"
       runtime       = "nodejs14.x"

       source_code_hash = filebase64sha256("lambda_function.zip")

       filename = "lambda_function.zip"
       timeout  = 30
     }

     resource "aws_lambda_permission" "allow_connect_invoke" {
       statement_id  = "AllowExecutionFromConnect"
       action        = "lambda:InvokeFunction"
       function_name = aws_lambda_function.connect_lambda.function_name
       principal     = "connect.amazonaws.com"
     }
     ```

3. **Create Lambda Function Code**:
   - Create a simple Lambda function in JavaScript (`index.js`):
     ```javascript
     exports.handler = async (event) => {
       console.log("Event: ", event);
       const response = {
         statusCode: 200,
         body: JSON.stringify('Hello from Lambda!'),
       };
       return response;
     };
     ```

   - Zip the Lambda function code:
     ```sh
     zip lambda_function.zip index.js
     ```

4. **Deploy Terraform Configuration**:
   - Initialize Terraform and apply the configuration:
     ```sh
     terraform init
     terraform apply
     ```

This configuration ensures that both the assume role policy and the Lambda policy are stored in separate JSON files inside the `policy` folder and are referenced correctly in the Terraform script using the `file` function. Adjust the paths and filenames as necessary to fit your directory structure and requirements.
