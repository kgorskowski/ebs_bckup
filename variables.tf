# declare necessary variables

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
variable "AWS_REGION" {
  description = "AWS Region where the Lambda function shall run"
}
variable "EC2_INSTANCE_TAG" {
  description = "Tag to identify the EC2 target instances of the Lambda Function"
}
variable "RETENTION_DAYS" {
  default = 5
  description = "Numbers of Days that the EBS Snapshots will be stored (INT)"
}
variable "unique_name" {
  description = "Enter Unique Name to identify the Terraform Stack (lowercase)"
}

variable "stack_prefix" {
  default = "ebs_bckup"
  description = "Stack Prefix for resource generation"
}

variable "cron_expression" {
  description = "Cron expression for firing up the Lambda Function"
}
