output "aws_iam_role_arn" {
  value = "${aws_iam_role.ebs_bckup-role-lambdarole.arn}"
}


output "lambda_function_name" {
  value = "${aws_lambda_function.ebs_bckup_lambda.function_name}"
}
