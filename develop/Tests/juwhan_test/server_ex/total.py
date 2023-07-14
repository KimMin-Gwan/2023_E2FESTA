from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB에 연결
client = MongoClient('mongodb+srv://sunjuwhan:ans693200@sunjuwhan.soaegl1.mongodb.net/')
db = client['test_sun']
collection = db['test']

# 데이터 전송 엔드포인트
@app.route("/rcv", methods=["POST"])
def receive_data():
    data = {"id","2번째 하는 거입니다."}
    # document = {'name': 'John', 'age': 30}
    # result = collection.insert_one(document)
    # 데이터를 데이터베이스에 저장 또는 처리하는 로직 구현
    collection.insert_one(data)
    return "Data received and saved to the database."

# 데이터 요청 엔드포인트

@app.route("/ssv")
def send_data():
    data = collection.find()
    # 데이터 가공 및 출력 로직 구현
    result = []
    for document in data:
        result.append(document)
    return {'data': result}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)