# master.py
"""
* Program Purpose and Features :
* - for Running Surver 
* - This file will run in AWS
* Author : Juwhan Kim
* First WriJuwhante Date : 2023.07.16
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* Juwhan KIM			2023.07.16      v0.10	    make file
* 
"""
from typing import Any
from flask import Flask, request
from pymongo import MongoClient# pymongo 임포트

class Server:
    
    def __init__(self):
        self.app = Flask(__name__)
        self.client=MongoClient('mongodb+srv://sunjuwhan:ans693200@sunjuwhan.soaegl1.mongodb.net/')
        self.db=self.client['test_sun']
        self.collection=self.db['test']
        # self.client=MongoClient('mongodb+srv://sbag00385:qlalfQjsgh486@cluster0.xpb7mqw.mongodb.net/') #데이터베이스 연결
        # self.db=self.client['flag'] #데이터베이스 이름 : flag
        # self.collection=self.db['kate'] #컬렉션(kate) 관리함수 실행
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
            print("===ids===",ids)

            query = {ids[0]:ids[1],"KEY":ids[2]}
            result = self.collection.find(query)
            list_reuslt=[]
            for document in result:
                list_reuslt.append(document)


            for i in range(len(list_reuslt)):
                print(list_reuslt[i])
                

            print("그중 전달받은 key값은",ids[2],"이고 이에 해당하는 데이터는")
            print(list_reuslt[0]["DATA_1"])
            
            return list_reuslt[0]["DATA_1"]
        
        
    def strat_server(self):
        self.app.run(host="0.0.0.0", port="8080")


if __name__=="__main__":
    server=Server()
    server.strat_server()

    
