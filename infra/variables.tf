variable "aws_region" {
  description = "Regiao AWS"
  type        = string
}

variable "project_name" {
  description = "Nome do projeto/servico (prefixo dos recursos)"
  type        = string
}

# SQS
variable "sqs_queue_name" {
  description = "Nome da fila SQS"
  type        = string
}

# DynamoDB
variable "dynamodb_table_name" {
  description = "Nome da tabela DynamoDB"
  type        = string
}
