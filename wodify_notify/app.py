import json
from requests import get
from bs4 import BeautifulSoup
import boto3
import os

phone_numbers = os.environ['PHONE_NUMBERS']

def lambda_handler(event, context):

    sns = boto3.client('sns')
    # https://www.dataquest.io/blog/web-scraping-beautifulsoup/

    url = 'http://crossfit3000.com/wod/'
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)
    wod_containers = html_soup.find_all('div', class_='blog_head')
    # print(type(wod_containers))
    # print(len(wod_containers))

    # print(wod_containers[0].h3)
    latest_wod_post = wod_containers[0].h3

    for a in latest_wod_post.find_all('a', href=True):
        # latest_wod_post_url = 'http://crossfit3000.com/friday-1st-feb/'
        latest_wod_post_url = a['href']
        print("Found the URL:", latest_wod_post_url)

    response_latest_wod = get(latest_wod_post_url)
    latest_wod_html_soup = BeautifulSoup(response_latest_wod.text, 'html.parser')
    latest_wod_details = latest_wod_html_soup.find('div', class_='blog_post_item_description').text

    print(latest_wod_details)

    sender_id = 'Wodify'
    sms_message = latest_wod_details + " " + latest_wod_post_url

    sns.publish(PhoneNumber=phone_numbers, Message=sms_message,
                MessageAttributes={'AWS.SNS.SMS.SenderID': {'DataType': 'String', 'StringValue': sender_id},
                                   'AWS.SNS.SMS.SMSType': {'DataType': 'String', 'StringValue': 'Promotional'}})

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Sent details for WOD:" + latest_wod_post_url,
            # "location": ip.text.replace("\n", "")
        }),
    }
