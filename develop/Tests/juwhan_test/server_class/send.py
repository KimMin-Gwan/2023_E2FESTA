
#url 을 전송하는 방법

import requests

url = 'http://127.0.0.1:8000/rcv?id=ID&id=SUB&id=3번째 id부분입니다.'

response = requests.get(url)