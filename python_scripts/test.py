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
