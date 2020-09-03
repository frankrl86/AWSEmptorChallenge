# AWS Emptor Challenge

We recommend you use ​Serverless Framework​ and ​Python 3.7​. Feel free to use additional ​Serverless Framework plugins​ if needed or desired. If you are more comfortable in a common language other than Python, you may use that instead.
This project builds on itself; each version is an evolution of the previous version. See how far you are able to go in a reasonable amount of time (< 8-10 hours). It is not required to complete all versions to have a good submission.
While this project should be entirely covered by the ​AWS Free Tier​, please make sure that you delete any deployments when no longer needed to ensure that you do not get charged for them.


## First Version (Completed)

Write and deploy a ​Lambda​ function that receives a URL as an argument,
and makes a request to that URL. The Lambda function extracts the title from the HTML document in the response and returns it to the caller. (You can use ​requests​ module for making the request.)

Solution (First Version):
```bash
def lambda_handler(event, context):
    try:
        url = event['url']
        response = requests.get(url)
        html = response.text
        title = html[html.find('<title>') + 7: html.find('</title>')]
        return {
            'statusCode': 200,
            'body': json.dumps({
                "title": title,
            })
        }
    except requests.RequestException as e:
        return
        {
            'statusCode': 400,
            'body': json.dumps('Error returning the title of the URL')
        }
```

## Second Version (Completed)

■ Refactor the function to store the response body to an ​S3 bucket​.
■ Store the extracted title as a record in a ​DynamoDB table.
■ Return the extracted title and the S3 URL of the stored response object.

Solution (Second Version):
```bash
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
```

## Third Version (In Progress)
