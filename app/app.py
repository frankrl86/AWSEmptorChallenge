import json
import requests


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
