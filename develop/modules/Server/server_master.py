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
        self.client=MongoClient("mongodb+srv://sbag00385:<password>@cluster0.xpb7mqw.mongodb.net/")# 데이터베이스 연결
        self.db = self.client['flag']# 데이터베이스 이름 : flag

        self.transmit('kate')# for send/recv 함수
        
    # class 실행 위한 함수
    def __call__(self):
        pass


    
    def transmit(self,collection):
        @self.app.route("/rcv",methods=["POST"])
        def post():
            data=request.json
            resp = self.send_db(collection,data)
            return {'id':'resp'}
            

    def send_db(self, collection, jsn):
        mycol=self.db[collection]# 컬렉션
        jsn_id = mycol.insert_one(jsn).inserted_id# 삽입
        print('_id:', jsn_id)
        return jsn_id
        
    
    # 서버 url
    def run_server(self):
        self.app.run(host='0.0.0.0',port=7777)

if __name__=="__main__":
    server=Server_Master()
    server.run_server()                                         