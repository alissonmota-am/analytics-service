################################################################################
# SQS Queue
################################################################################
module "sqs_dynamodb" {
  source = "../../toggle-master-infra/modules/sqs_dynamodb"

  project_name = var.project_name
  queue_name   = var.sqs_queue_name
  table_name   = var.dynamodb_table_name
}
