import boto3

s3 = boto3.resource('s3')
ssm = boto3.client('ssm','eu-central-1')
bucket_name = ssm.get_parameter(Name='coursera-course-bucket-name', WithDecryption=False)['Parameter']['Value']

bucket = s3.Bucket(bucket_name)

for obj in bucket.objects.all():
    print(obj.key, obj.last_modified)
    

s3_client = boto3.resource('s3').meta.client
    
