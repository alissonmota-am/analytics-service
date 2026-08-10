################################################################################
# SQS Queue
################################################################################
module "sqs" {
  source = "git::https://github.com/alissonmota-am/toggle-master-infra.git//modules/sqs?ref=develop"

  queue_name = var.sqs_queue_name
}

################################################################################
# DynamoDB Table
################################################################################
module "dynamodb" {
  source = "git::https://github.com/alissonmota-am/toggle-master-infra.git//modules/dynamodb?ref=develop"

  table_name    = var.dynamodb_table_name
  hash_key      = "event_id"
  hash_key_type = "S"
}
