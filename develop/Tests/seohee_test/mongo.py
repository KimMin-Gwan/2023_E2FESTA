from pymongo import MongoClient# pymongo 임포트
#import datetime

client=MongoClient('')

db = client.hobby# 데이터베이스 이름 : hobby

#print(client.list_database_names())#왜 config 안나오지?
#print(client.dbdb.list_collection_names())

 

# 삽입 ----------------------------------------------
#data = {
#    'author' : 'hun',
#    'text' : 'mongoDB is what..?',
#    'tags' : ['mongoDB', 'python', 'pymongo']
#}
#dpInsert = db.posts.insert_one(data)

#data = {
#    'author' : 'lee',
#    'text' : 'mongoDB here',
#    'tags' : ['mongoDB', 'python', 'pymongo']
#}
#dpInsert = db.posts.insert_one(data)

# 읽기 -----------------------------------------------
#for d in db['posts'].find():
#    print(type(d))
#    print(d['author'], d['text'], d['tags'])

# 'author':'hun'인 데이터 조회
#print(db.posts.find_one({'author':'hun'})['text'])

# text 칼럼을 제외하고 데이터 가져오기
#for d in db['posts'].find({}, {'text' : 0}):
#    print(d)


# 수정 ---------------------------------------------------------
#db.posts.update_one({'author':'lee'},{'$set':{'author':'LEE'}})

#삭제 --------------------------------------------------------
#db.posts.delete_one({'author':'LEE'})

client.close()