import requests
from flask import jsonify

url='http://127.0.0.1:7777/rcv'
# post={'id':'20'}
# #resp=jsonify(post)
# respone=requests.post(url,json=post)
# print(respone)
# #print(respone.json())

response=requests.get(url)

# response.raise_for_status()
print(response)