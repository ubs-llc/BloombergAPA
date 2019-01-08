import time
import os
import sys

import requests
from bs4 import BeautifulSoup


class Document:
    def __init__(self, name, link):
        self.filename = name
        self.link = link


base_url = 'https://www.bloombergapa.com'
url = 'https://www.bloombergapa.com/historyfiles'
path = os.path.dirname(os.path.abspath(__file__)) + '\\Data\\'

while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    parsed_documents = set()
    tags = soup.find(class_='tab-content').find_all('a')
    documents = set(map(lambda x:Document(x.text.replace(':',''), x['href']), tags))
    print(sys.getsizeof(parsed_documents))
    for doc in documents - parsed_documents:
        r = requests.get(base_url + doc.link)
        if r.status_code==200:
            content = r.text
            with open(path + doc.filename, 'w+') as file:
                file.write(r.text)
        parsed_documents.add(doc)
    time.sleep(60)