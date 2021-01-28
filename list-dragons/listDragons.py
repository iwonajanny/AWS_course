import boto3
import json

s3 = boto3.client('s3','eu-central-1')
ssm = boto3.client('ssm', 'eu-central-1')
bucket_name = ssm.get_parameter( Name='coursera-course-bucket-name',WithDecryption=False)['Parameter']['Value']
file_name = ssm.get_parameter( Name='coursera-file-name',WithDecryption=False)['Parameter']['Value']

def listDragons(event, context):
    
    expression = "select * from s3object s"

    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        if 'dragonName' in event['queryStringParameters']:
            expression = "select * from S3Object[*][*] s where s.dragon_name_str =  '" + event["queryStringParameters"]['dragonName'] + "'"
        if 'family' in event['queryStringParameters']:
            expression = "select * from S3Object[*][*] s where s.family_str =  '" + event["queryStringParameters"]['family'] + "'"

    result = s3.select_object_content(
            Bucket=bucket_name,
            Key=file_name,
            ExpressionType='SQL',
            Expression=expression,
            InputSerialization={'JSON': {'Type': 'Document'}},
            OutputSerialization={'JSON': {}}
    )
    
    records = ''
    for event in result['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
   
    return {
        "statusCode": 200,
        "body": json.dumps(records)
    }
        