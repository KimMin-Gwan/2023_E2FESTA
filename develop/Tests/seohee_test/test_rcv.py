
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

    def transmit(self,collection):
        # 데이터 반환(serv->clnt)
        @self.app.route("/rcv")
        def post():
            id = '20'
            resp = self.rcv_db(collection,id)
            return {'id':'resp'}
    
# 데이터 반환 함수
    def rcv_db(self, collection,id):
        try:
            mycol = self.db[collection]
            data=mycol.find_one({'id':id})
            return data
        except Exception as e:
            print("Error :", str(e))
            return -1

    # 서버 url
    def run_server(self):
        self.app.run(host='0.0.0.0',port=7777)

if __name__=="__main__":
    server=Server_Master()
    server.run_server()    