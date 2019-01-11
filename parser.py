import time
import os
import sys

import requests
from bs4 import BeautifulSoup
import boto3

s3 = boto3.resource('s3')


class Document:
    def __init__(self, name, link):
        self.filename = name
        self.link = link


base_url = 'https://www.bloombergapa.com'
url = 'https://www.bloombergapa.com/slicefiles'
path = os.path.dirname(os.path.abspath(__file__)) + '\\Data\\'

BUCKET_NAME = 'ib-bucket-aws'

while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    last_document = None
    tag = soup.find(class_='tab-content').find('a')
    document = Document(tag.text.replace(':',''), tag['href'])

    if last_document != document:
        r = requests.get(base_url + document.link)
        if r.status_code==200:
            content = r.text
            with open(path + document.filename, 'w+') as file:
                file.write(r.text)
            obj = s3.Object(BUCKET_NAME, 'BloombergAPA/' + document.filename)
            obj.put(Body=r.content)
        last_document = document
    time.sleep(60)