#server_master.py
"""
* Program Purpose and Features :
* - Server_Master 
* - This file will run in AWS
* Author : MG KIM
* First Write Date : 2023.07.11
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* MG KIM			2023.07.11      v0.10	    make file
"""
from flask import Flask, request
from pymongo import MongoClient# pymongo 임포트

class Server_Master:
    # 생성자
    def __init__(self):
        self.app = Flask(__name__)
        self.client=MongoClient("mongodb+srv://sunjuwhan:ans693200@sunjuwhan.soaegl1.mongodb.net/")# 데이터베이스 연결
        # self.db = self.client['test_sun']# 데이터베이스 이름 : flag
        self.get()
        self.data=[]
        # self.transmit('test')# for send/recv 함수
        
    # class 실행 위한 함수
    def __call__(self):
        pass


    
    def transmit(self,collection):
        @self.app.route("/rcv",methods=["POST"])
        def post():
            data=request.json
            resp = self.send_db(collection,data)
            return {'id':'resp'}

    def get(self):
        @self.app.route("/mytest",methods=["GET"])
        def GET():
            db=self.client['test_sun']
            collection=db['test']
            query={'name':'John'}
            result=collection.find(query)
            for document in result:
                print(document)
    # 데이터 가공 및 출력 로직 구현

    def send_db(self, collection, jsn):
        mycol=self.db[collection]# 컬렉션
        jsn_id = mycol.insert_one(jsn).inserted_id# 삽입r
        print('_id:', jsn_id)
        return jsn_id
        

    # 서버 url
    def run_server(self):
        self.app.run(host='0.0.0.0',port=5000)

if __name__=="__main__":
    server=Server_Master()
    server.run_server()                                         