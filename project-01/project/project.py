import boto3
import click
from botocore.exceptions import ClientError

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
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List object in se bucket"
#pass == Place holder
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

## New command to automate the website
@cli.command('setup-bucket')
@click.argument('bucket')
def set_bucket(bucket):
    "Create and configure S3 bucket"
    s3_bucket = None
    ##ctrl + r = history
    #s3_bucket = s3.create_bucket(
    #Bucket=bucket,
    #CreateBucketConfiguration={'LocationConstraint': session.region_name}

#    )

##S3 BUCKET WITH EXCEPTION
    try:
        s3_bucket = s3.create_bucket(
            Bucket=bucket,

            CreateBucketConfiguration={'LocationConstraint': session.region_name}
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)
        else:
            raise e


##Create a policy
    policy = """
    {
    "Version":"2012-10-17",
    "Statement":[
     {
       "Sid":"PublicReadGetObject",
       "Effect":"Allow",
       "Principal": "*",
       "Action":["s3:GetObject"],
       "Resource":["arn:aws:s3:::%s/*"]
     }
    ]
    }
    """ % s3_bucket.name
## Attach policy
    pol = s3_bucket.Policy() ##Get the policy object (resource)
    policy = policy.strip()  ##Remove a new line at the bigining and at the end of the policy.
    pol.put(Policy=policy)   ##Attach the policy to the bucket

### Website configure
    ws = s3_bucket.Website()
#### https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#bucketpolicy
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
