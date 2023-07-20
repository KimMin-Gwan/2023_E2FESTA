
#url 을 전송하는 방법

import requests

def send():
    url = 'http://172.31.7.94:5000/'
    response = requests.get(url)
    
send()