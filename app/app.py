import json
import requests
import boto3

#First Version
# def lambda_handler(event, context):
#     try:
#         url = event['url']
#         response = requests.get(url)
#         html = response.text
#         title = html[html.find('<title>') + 7: html.find('</title>')]
#         return {
#             'statusCode': 200,
#             'body': json.dumps({
#                 "title": title,
#             })
#         }
#     except requests.RequestException as e:
#         return
#         {
#             'statusCode': 400,
#             'body': json.dumps('Error returning the title of the URL')
#         }

#Second Version
def lambda_handler(event, context):
    try:
        url = event['url']
        response = requests.get(url)
        html = response.text
        title = html[html.find('<title>') + 7: html.find('</title>')]

        dynamodb = boto3.resource('dynamodb')
        s3 = boto3.resource('s3')
        bucket_name = "s3urls"
        table_url = dynamodb.Table('tb_url')
        table_url.put_item(
            Item={
                'url': url,
                'title': title,
            }
        )
        s3.Bucket(bucket_name).put_object(Key=url, Body=html)

        return {
            'statusCode': 200,
            'body': json.dumps({
                "title": title,
                "url": url,
            })
        }
    except requests.RequestException as e:
        return
        {
            'statusCode': 400,
            'body': json.dumps('Error returning Title and URL')
        }