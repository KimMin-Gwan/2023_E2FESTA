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

# 서버 관리 클래스
class Server_Master:
    # 생성자
    def __init__(self):
        self.app = Flask(__name__)
        # 데이터베이스 연결
        self.client=MongoClient("mongodb+srv://sbag00385:<password>@cluster0.xpb7mqw.mongodb.net/")
        # 데이터베이스 이름 : flag
        self.db = self.client['flag']
        # ''라는 컬렉션 관리 함수 실행
        self.transmit('kate')
        
    # class 실행 위한 함수
    def __call__(self):
        pass
    
    def transmit(self,collection):
        # # 데이터  추가(clnt->serv)
        # @self.app.route("/send",methods=["POST"])
        # def post():
        #     data=request.json
        #     sendp = self.send_db(collection,data)
        #     return {'id':'sendp'}
       
        # 데이터 반환(serv->clnt)
        @self.app.route("/rcv")
        def get():
            id = '20'
            resp = self.rcv_db(collection,id)
            return {'id':'resp'}
       
        # # 데이터 삭제(clnt->serv)
        # @self.app.route("/del",methods=["DELETE"])
        # def delete():
        #     data=request.json
        #     delp = self.del_db(collection,data)
        #     return {'id':'resp'}
       
        # # 데이터 수정(clnt->serv)
        # @self.app.route("/change",methods=["PATCH"])
        # def change():
        #     data=request.json
        #     changp = self.change_db(collection,data)
        #     return {'id':'resp'}


    # # 데이터 전송 함수
    # def send_db(self, collection, jsn):
    #     mycol=self.db[collection]# 컬렉션
    #     jsn_id = mycol.insert_one(jsn).inserted_id# 삽입
    #     print('_id:', jsn_id)
    #     return jsn_id
    
    # 데이터 반환 함수
    def rcv_db(self, collection,id):
        try:
            mycol = self.db[collection]
            data=mycol.find_one({'id':id})
            return data
        except Exception as e:
            print("Error :", str(e))
            return -1

    # # 데이터 삭제 함수
    # def del_db(self, collection, data):
    #     pass

    # # 데이터 수정 함수
    # def change_db(self, collection, data):
    #     pass

    # 서버 url
    def run_server(self):
        self.app.run(host='0.0.0.0',port=7777)

if __name__=="__main__":
    server=Server_Master()
    server.run_server()                                         