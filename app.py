import boto3

s3 = boto3.resource('s3','eu-central-1').meta.client
ssm = boto3.client('ssm', 'eu-central-1')
bucket_name = ssm.get_parameter( Name='coursera-course-bucket-name',WithDecryption=False)['Parameter']['Value']
file_name = ssm.get_parameter( Name='coursera-file-name',WithDecryption=False)['Parameter']['Value']

def listDragons():
    
    expression = "select * from s3object s"

    result = s3.select_object_content(
            Bucket=bucket_name,
            Key=file_name,
            ExpressionType='SQL',
            Expression=expression,
            InputSerialization={'JSON': {'Type': 'Document'}},
            OutputSerialization={'JSON': {}}
    )
    
    for event in result['Payload']:
        if 'Records' in event:
            print(event['Records']['Payload'].decode('utf-8'))
   
listDragons()