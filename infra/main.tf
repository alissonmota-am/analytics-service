################################################################################
# SQS Queue
################################################################################
module "sqs_dynamodb" {
  source = "git::https://github.com/alissonmota-am/toggle-master-infra.git//modules/sqs_dynamodb?ref=develop"

  project_name = var.project_name
  queue_name   = var.sqs_queue_name
  table_name   = var.dynamodb_table_name
}
