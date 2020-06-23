#!/usr/bin/env python
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
    print(instance.id, instance.state)
