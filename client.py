import boto3

client = boto3.client('s3')
ssm = boto3.client('ssm','eu-central-1')
bucket_name = ssm.get_parameter(Name='coursera-course-bucket-name', WithDecryption=False)['Parameter']['Value']

response = client.list_objects(Bucket = bucket_name)

for content in response['Contents']:
    obj_dict = client.get_object(Bucket = bucket_name, Key = content['Key'])
    print(content['Key'], obj_dict['LastModified'])
    
