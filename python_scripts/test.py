provider "aws" {
  region = "us-west-2"
}

resource "aws_connect_instance" "example" {
  identity_management_type = "CONNECT_MANAGED"
  inbound_calls_enabled    = true
  outbound_calls_enabled   = true
}

resource "aws_connect_contact_flow" "example" {
  instance_id = aws_connect_instance.example.id
  name        = "HCP - Agent Transfer"
  description = "Contact flow for agent transfer"
  content     = file("path/to/contact_flow.json")
  type        = "CONTACT_FLOW"
}

resource "aws_connect_queue" "example" {
  instance_id          = aws_connect_instance.example.id
  name                 = "ExampleQueue"
  description          = "Example description"
  hours_of_operation_id = "your_hours_of_operation_id"
  max_contacts         = 10
  quick_connect_ids    = ["your_quick_connect_id"]
  outbound_caller_config {
    outbound_caller_id_name    = "Caller ID Name"
    outbound_caller_id_number_id = "your_outbound_caller_id_number_id"
    outbound_flow_id           = "your_outbound_flow_id"
  }
}

resource "aws_connect_routing_profile" "example" {
  instance_id              = aws_connect_instance.example.id
  name                     = "ExampleRoutingProfile"
  description              = "Routing profile description"
  default_outbound_queue_id = aws_connect_queue.example.id
  queue_configs {
    queue_id    = aws_connect_queue.example.id
    priority    = 1
    delay       = 0
  }
  media_concurrencies {
    channel     = "VOICE"
    concurrency = 1
  }
}

resource "aws_lambda_function" "example" {
  function_name = "JAP-PROD-serverlessrepo-s-InvokeTelephonyIntegrati-5Asv2AMrlNmG"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "index.handler"
  runtime       = "nodejs14.x"
  source_code_hash = filebase64sha256("lambda.zip")
  filename      = "path/to/lambda.zip"
  environment {
    variables = {
      methodName = "createTransferVC"
    }
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  inline_policy {
    name = "lambda_policy"
    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Action = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          Effect   = "Allow",
          Resource = "*"
        },
        {
          Action = [
            "connect:StartOutboundVoiceContact",
            "connect:StopContact",
            "connect:GetContactAttributes"
          ],
          Effect   = "Allow",
          Resource = "*"
        }
      ]
    })
  }
}

resource "aws_connect_contact_attribute" "example" {
  instance_id = aws_connect_instance.example.id
  name        = "voiceCallId"
  description = "Attribute for storing voice call ID"
}

resource "aws_connect_quick_connect" "example" {
  instance_id = aws_connect_instance.example.id
  name        = "ExampleQuickConnect"
  description = "Quick connect for transferring calls"
  quick_connect_config {
    quick_connect_type = "USER"
    user_config {
      user_id        = "user_id"
      contact_flow_id = aws_connect_contact_flow.example.id
    }
  }
}
