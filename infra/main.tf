# notifications-service infrastructure, applied from main by the platform pipeline.
# Sandbox note: the stack in agent-scope/phase1/terraform creates these resources; this file
# is the service's own declaration of them (evidence for the map builder), not applied alone.
provider "aws" {
  region = "us-east-2"
}

resource "aws_cloudwatch_log_group" "staging" {
  name = "notif-staging-logs"
}

resource "aws_cloudwatch_log_group" "prod" {
  name = "notif-prod-logs"
}

resource "aws_secretsmanager_secret" "sendgrid" {
  name = "notif-sendgrid-key"
}

data "aws_iam_role" "task" {
  name = "agentscope-task-notifications"
}

data "aws_iam_role" "events" {
  name = "payments-shared-role"
}
