import requests
import numpy as np

# 3차원 배열 생성 (예시)
array_3d = np.random.randint(0, 10, size=(3, 4, 5))

# JSON 직렬화
data = {'array_3d': array_3d.tolist()}

# 서버 URL
url = "http://127.0.0.1:5000/receive_array"
print(data)
# POST 요청 보내기
response = requests.post(url, json=data)

print(response.text)