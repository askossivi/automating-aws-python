import boto3
import click

#session
session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')
from botocore.exceptions import ClientError


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

#Create bucket
@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
	"Create and configure S3 bucket"
	s3_bucket = None

	try:
		s3_bucket = s3.create_bucket(Bucket=bucket,
			ACL='public-read-write',
			CreateBucketConfiguration={'LocationConstraint': session.region_name}
			)
	except ClientError as e:
		if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
			s3_bucket = s3.Bucket(bucket)
		else:
			raise e

#Create and attach policy
	policy = """
	{
	"Version":"2012-10-17",
	"Statement":[
	{
	  "Sid":"PublicReadGetObject",
	  "Effect":"Allow",
	  "Principal": "*",
	  "Action":["s3:GetObject"],
	  "Resource":["arn:aws:s3:::%s/*"
	  ]
	}
	]
	}
	""" % s3_bucket.name
#Attach Policy
	pol = s3_bucket.Policy() #This to get the policy object
	policy = policy.strip()
	pol.put(Policy=policy)

#3- Set up website configuration
	ws = s3_bucket.Website() #resource

#ws.put(WebsiteConfiguration={}) ##Set up website configuration
	ws.put(WebsiteConfiguration={
	        'ErrorDocument': {
	            'Key': 'error.html'
	        },
	        'IndexDocument': {
	            'Suffix': 'index.html'
	        }
	 })

	return


if __name__ == '__main__':
	cli()
