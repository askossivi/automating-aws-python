###SCRIPT WITH CLICK ##

import boto3
import click

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)

if __name__ == '__main__':
	list_buckets()








##New Script

import boto3
import click

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "Project deploys website to AWS"
pass


@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
#pass == Place holder
    for bucket in s3.buckets.all():
        print(bucket)


@cli.command('list-bucket-objects')
def list_bucket_objects():
    "List object in se bucket"
#pass == Place holder
    for obj in s3.Bucket('awsautomatingaskossivi-boto3').objects.all():
        print(obj)


if __name__ == '__main__':
    cli()
