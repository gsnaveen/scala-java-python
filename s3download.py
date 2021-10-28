
import os
import boto3
import json

os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
os.environ["REGION"] = 'us-west-2'

sts_client = boto3.client('sts')

assumed_role_object=sts_client.assume_role(
   RoleArn="arn:aws:iam::9999:role/xyz.abc.who",
   RoleSessionName="AssumeRoleSession1"
)

credentials=assumed_role_object['Credentials']

session = boto3.session.Session(
   aws_access_key_id=credentials['AccessKeyId'],
   aws_secret_access_key=credentials['SecretAccessKey'],
   aws_session_token=credentials['SessionToken'],
)

s3  = session.resource('s3')

for bucket in s3.buckets.all():
   if bucket.name == 'skyline-datalake-files-us-west-2-prod':
       print(bucket.name)
       for obj in bucket.objects.all():
           print(obj.bucket_name,obj.key)

           # bucketd = s3.Bucket(bucket.name)
           # with open('./data/' + obj.key, 'wb') as data:
           #     bucketd.download_fileobj(obj.key, data)

           s3.Bucket(bucket.name).download_file(obj.key, './downloads/' + obj.key)
