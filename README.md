Hi.
Here comes my next experiments in Lambda and Terraform.
This is based on this blogpost https://serverlesscode.com/post/lambda-schedule-ebs-snapshot-backups-2/
and again I take no credit for the idea and/or the code.
I just wanted to make this more portable and more easily reproducable.
That's about it.
If you like it, install Terraform, clone the repo, copy the the .example file to terraform.tfvars and fill in your variables.
Then you run "terraform get" to initialize the modules, "terraform plan" to see what resources will be created and if you are fine with it, finally "terraform apply" to create the resources.
To use this script, you need to add a Tag with the value "Backup" to the Instances you want to be targeted by the Function. The Name of the Tag doesn't matter, but if your Instance is not tagged, it will be ignored and no snapshot will be created.

The Lambda function is triggered by a scheduled CloudWatch event. It looks for all Instances with the "Backup"-Tag, then checks the matching Instances for mounted EBS Volumes.
It will then create a snapshot of the Volume, name the snapshot after the Instance ID and the day the snapshot was taken and add the "DeleteOn" Tag with the expiration date of the snapshot.
Then it compares the actual date with the "DeleteOn" Tag of the existing snapshots and deletes the one wich are out of the retention span.
Disclaimer: If you have a large number of Instances and/or snapshots, I cannot guarantee that you won't hit any Lambda timeouts. With just a few Instances you should be fine.
Disclaimer II: As with every mechanism where you take a snapshot of a running machine, nobody can guarantee that the snapshots are absolutely consistent. So be aware that this is not a 100% secure way to take snapshots especially when you have a high load application. Amazon advises you to unmount root volumes before taking a snapshot, see here http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-creating-snapshot.html
