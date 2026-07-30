output "sqs_queue_url" {
  description = "URL da fila SQS (usar em AWS_SQS_URL)"
  value       = module.sqs_dynamodb.queue_url
}

output "sqs_queue_arn" {
  description = "ARN da fila SQS"
  value       = module.sqs_dynamodb.queue_arn
}

output "dynamodb_table_name" {
  description = "Nome da tabela DynamoDB"
  value       = module.sqs_dynamodb.table_name
}

output "dynamodb_table_arn" {
  description = "ARN da tabela DynamoDB"
  value       = module.sqs_dynamodb.table_arn
}
