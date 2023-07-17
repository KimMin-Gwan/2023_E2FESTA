
#url 을 전송하는 방법

import requests

def send():
    
    url = 'http://127.0.0.1:8000/rcv?id=ID&id=TRF&id=1'

    response = requests.get(url)
    
    
    
send()