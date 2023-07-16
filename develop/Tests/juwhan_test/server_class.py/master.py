from typing import Any
from flask import Flask, request
from pymongo import MongoClient# pymongo 임포트

class Server:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.client=MongoClient('mongodb+srv://sunjuwhan:ans693200@sunjuwhan.soaegl1.mongodb.net/')
        self.db=self.client['test_sun']
        self.collection=self.db['test']

        self.route() #main클래스 실행

    def __call__(self):
        pass
    def route(self):#비콘으로 부터 key값을 받아온 상황이라고 생각해보자
        @self.app.route('/')
        def main_htp():
            return "여기는 SUN의 data_base입니다."

        @self.app.route('/rcv',methods=['GET'])#http 로 접속시에는 127.0.0.1:8000/rcv?id=123&id=abc&id=... 하면 id값이 123이 들어가게된다.
        def get():
            #넣어줘야할 데이터는 http://127.0.0.1:8000/rcv?id=ID&id=SUB&id=여기에 이제 key값을 넣어서 몇번째 비콘인지 찾는거지
            #현재 data frame 이 {'_id': ObjectId('64b394a993c1322d8377cefa'), 'ID': 'SUB', 'KEY': '1', 'DATA_1': '영남대방향'}
            #이런 형태로 저장되어있음
            ids=request.args.getlist('id')
            client = MongoClient('mongodb+srv://sunjuwhan:ans693200@sunjuwhan.soaegl1.mongodb.net/')
            # 데이터베이스 선택 (기본적으로 'test' 데이터베이스를 사용)
            db = client['test_sun']
            collection = db['test']
            query = {ids[0]:ids[1]}
            result = collection.find(query)
            list_reuslt=[]
            for document in result:
                list_reuslt.append(document)

            print(list_reuslt)



            return "he"


        

    
