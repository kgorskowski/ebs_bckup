import boto3
import ConfigParser
import botocore
import datetime
import re
import collections

config = ConfigParser.RawConfigParser()
config.read('./vars.ini')

print('Loading Backup function')

def lambda_handler(event, context):
    EC2_INSTANCE_TAG = config.get('main', 'EC2_INSTANCE_TAG')
    retention_days = config.getint('main', 'RETENTION_DAYS')
    aws_region = event['region']
    account = event['account']
    ec = boto3.client('ec2', region_name=aws_region)
    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag-value', 'Values': [EC2_INSTANCE_TAG]},
        ]
    )['Reservations']
    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
            ], [])

    to_tag = collections.defaultdict(list)

    for instance in instances:
        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None:
                # skip non EBS volumes
                continue
            vol_id = dev['Ebs']['VolumeId']
            instance_id=instance['InstanceId']
            print("Found EBS Volume %s on Instance %s, creating Snapshot" % (vol_id, instance['InstanceId']))
            snap = ec.create_snapshot(
                Description="Snapshot of Instance %s" % instance_id,
                VolumeId=vol_id,
            )
            to_tag[retention_days].append(snap['SnapshotId'])

            for retention_days in to_tag.keys():
                delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
                snap = snap['Description'] + str('_')
                snapshot = snap + str(datetime.date.today())
                delete_fmt = delete_date.strftime('%Y-%m-%d')
                ec.create_tags(
                Resources=to_tag[retention_days],
                Tags=[
                {'Key': 'DeleteOn', 'Value': delete_fmt},
                {'Key': 'Name', 'Value': snapshot}
                ]
                )
        to_tag.clear()

    delete_on = datetime.date.today().strftime('%Y-%m-%d')
    filters = [
        {'Name': 'tag-key', 'Values': ['DeleteOn']},
        {'Name': 'tag-value', 'Values': [delete_on]},
    ]
    snapshot_response = ec.describe_snapshots(OwnerIds=['%s' % account], Filters=filters)
    for snap in snapshot_response['Snapshots']:
        print "Deleting snapshot %s" % snap['SnapshotId']
        ec.delete_snapshot(SnapshotId=snap['SnapshotId'])
