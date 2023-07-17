# import requests
# import json
# # url = 'http://127.0.0.1:5000/rcv'

# # response = requests.post(url)




# url = "http://127.0.0.1:5000/rcv"
# headers = {"Content-Type": "application/json"}  # Content-Type 설정
# data = {"name": "John"}  # 전송할 데이터

# response = requests.post(url, headers=headers, data=json.dumps(data))
# result = response.json()

# print(result)
# print(data)

# import requests

# url = 'http://127.0.0.1:5000/rcv'
# response = requests.get(url)
# print(response.text)









import requests
from flask import jsonify

url='http://127.0.0.1:5000/rcv'
#resp=jsonify(post)
respone=requests.post(url)
print(respone)