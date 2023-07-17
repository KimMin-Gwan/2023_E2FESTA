from pymongo import MongoClient
from flask import Flask, request
# MongoDB에 연결
app=Flask(__name__)

@app.route('/')
def b():
    return "hello world"

@app.route('/rcv',methods=['GET'])    #http 로 접속시에는 127.0.0.1:8000/rcv?id=123&id=abc 하면 id값이 123이 들어가게된다.
def a():
    ids=request.args.getlist('id')
    print("ids=====",ids)  #각 ids[0]으로 접근이 가능하다.
    client = MongoClient('mongodb+srv://sunjuwhan:ans693200@sunjuwhan.soaegl1.mongodb.net/')
    # 데이터베이스 선택 (기본적으로 'test' 데이터베이스를 사용)
    db = client['test_sun']
    collection = db['test']
    # document = {'name': 'John', 'age': 30}
    # result = collection.insert_one(document)
    # print(result.inserted_id)
    query = {ids[0]:ids[1]}
    result = collection.find(query)
    list_reuslt=[]
    for document in result:
        list_reuslt.append(document)
        # print(document)
    print(list_reuslt[0])
    print(list_reuslt[0]["DATA_1"])
    return "he"
    
if __name__=="__main__":
    app.run(host="127.0.0.1", port="8000")
