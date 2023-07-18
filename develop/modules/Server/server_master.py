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
* Author    		Date		    Version	    	History         code to fix
* Juwhan KIM	  2023.07.16         v0.10	        make file
* 
"""
from typing import *
from flask import Flask, request
from pymongo import MongoClient# pymongo 임포트


class Server:
    
    def __init__(self):
        self.app = Flask(__name__)
        self.client=MongoClient('mongodb+srv://sbag00385:<pw>@cluster0.xpb7mqw.mongodb.net/') #데이터베이스 연결
        self.db=self.client['flag'] #데이터베이스 이름 : flag
        self.collection=self.db['kate'] #컬렉션(kate) 관리함수 실행
        self.route() #main클래스 실행

    def __call__(self): #클래스부를때 사용
        pass


    def route(self): #비콘에서 key값을 받아온 상황이라고 가정
        @self.app.route('/')
        def main_htp():
            return
        
        #데이터 반환
        @self.app.route('/rcv',methods=['GET'])
        def get():
            ids=request.args.getlist('id')
            print("===ids===",ids)

            query = {ids[0]:ids[1],"KEY":ids[2]}
            result = self.collection.find(query)
            list_reuslt=[]
            for document in result:
                list_reuslt.append(document)

            for i in range(len(list_reuslt)):
                print(list_reuslt[i])

            print("그중 전달받은 key값은",ids[2],"이고 해당되는 데이터는")
            print(list_reuslt[0]["DATA"])
           
            return list_reuslt[0]["DATA"]
        

    def strat_server(self):
        self.app.run(host="127.0.0.1", port="7777")


if __name__=="__main__":
    server=Server() #
    server.strat_server() #서버 시작

    
