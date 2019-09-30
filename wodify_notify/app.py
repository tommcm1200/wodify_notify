import json
from requests import get
from bs4 import BeautifulSoup
import boto3
import os
import re

phone_numbers = os.environ['PHONE_NUMBERS']

def lambda_handler(event, context):

    sns = boto3.client('sns')
    # https://www.dataquest.io/blog/web-scraping-beautifulsoup/

    url = 'http://fitlabmelbourne.com/wod/'
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    wod_containers = html_soup.find_all("article", class_=re.compile("wp-show-posts-single"))

    # print(type(wod_containers))
    # print(len(wod_containers))

    latest_wod_post = wod_containers[0]
    latest_wod_details = latest_wod_post.find('div', class_="wp-show-posts-entry-content").text
    latest_wod_url = latest_wod_post.find('a')['href']
    print(latest_wod_details)
    print(latest_wod_url)

    sender_id = 'Wodify'
    sms_message = latest_wod_details + " " + latest_wod_url

    sns.publish(PhoneNumber=phone_numbers, Message=sms_message,
                MessageAttributes={'AWS.SNS.SMS.SenderID': {'DataType': 'String', 'StringValue': sender_id},
                                   'AWS.SNS.SMS.SMSType': {'DataType': 'String', 'StringValue': 'Promotional'}})

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Sent details for WOD:" + latest_wod_url,
            # "location": ip.text.replace("\n", "")
        }),
    }
