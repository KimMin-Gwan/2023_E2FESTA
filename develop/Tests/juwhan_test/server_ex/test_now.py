from pymongo import MongoClient
from flask import Flask, request
# MongoDB에 연결
app=Flask(__name__)



@app.route('/rcv')
def a():
    client = MongoClient('mongodb+srv://sunjuwhan:ans693200@sunjuwhan.soaegl1.mongodb.net/')
    # 데이터베이스 선택 (기본적으로 'test' 데이터베이스를 사용)
    db = client['test_sun']
    collection = db['test']
    # document = {'name': 'John', 'age': 30}
    # result = collection.insert_one(document)
    # print(result.inserted_id)
    query = {'name': 'John'}
    result = collection.find(query)
    list_reuslt=[]
    for document in result:
        list_reuslt.append(document)
        print(document)
    return 
    
if __name__=="__main__":
    app.run()
    