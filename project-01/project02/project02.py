import boto3
import click

#session
session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
	"PROJECT DEPLOYS STATIC WEBSITE TO AWS"
	pass

@cli.command('list-buckets')
def list_buckets():
	"List all buckets"
	for bucket in s3.buckets.all():
		print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket') #use of click argument to avoid hardcodint the bucket name
def list_bucket_objects(bucket):
	"List objects in an s3 bucket"
	for object in s3.Bucket(bucket).objects.all():
		print(object)


if __name__ == '__main__':
	cli()
