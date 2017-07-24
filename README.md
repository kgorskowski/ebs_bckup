# tf\_ebs\_bckup
## a Lambda-powered EBS Snapshot Terraform Module

A Terraform module for creating a Lambda Function that takes automatic snapshots of of all connected EBS volumes of correspondingly tagged instances.
The function is triggered via a CloudWatch event that can be freely configured by a cronlike expression.

## Input Variables:
- `EC2_INSTANCE_TAG` - All instances with this tag be backed up. Default is `"Backup"`
- `RETENTION_DAYS`   - Number of day the created EBS Snapshots will be stored, defaults to `5`
- `unique_name`      - Just a marker for the Terraform stack. Default is "v1"`
- `stack_prefix`     - Prefix for resource generation. Default is `ebs_bckup`
- `cron_expression`  - Cron expression for CloudWatch events. Default is `"22 1 * * ? *"`
- `regions`          - List of regions in which the Lambda function should run. Requires at least one entry (eg. `["eu-west-1", "us-west-1"]`)

## Outputs
Default outputs are `aws_iam_role_arn` with the value of the created IAM role for the Lambda function and the `lambda_function_name`

## Example usage
In your Terrafom `main.tf` call the module with the required variables.

```
module "ebs_bckup" {
  source = "github.com/kgorskowski/ebs_bckup"
  EC2_INSTANCE_TAG = "Backup"
  RETENTION_DAYS   = 10
  unique_name      = "v2"
  stack_prefix     = "ebs_snapshot"
  cron_expression  = "45 1 * * ? *"
  regions          = ["eu-west-1", "eu-central-1"]
}
```
