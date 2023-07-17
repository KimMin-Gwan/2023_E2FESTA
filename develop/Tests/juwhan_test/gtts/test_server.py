from flask import Flask, request

app=Flask(__name__)
@app.route("/")
def print_h():
    return "hello world"


@app.route("/test",methods=["POST"])
def test():
    # arg=request.json
    # print(arg['id'])
    return "hellow owlrd"

if __name__=='__main__':
    app.run(host='0.0.0.0',port=7777)