from flask import Flask, request
import Store

app = Flask(__name__)

n = 0
def next():
    global n
    n = n + 1
    return n

@app.route("/posts",methods=["POST"])
def create():
    js = request.get_json()
    t = js.get("text")
    if t != None:
        n = next()
        s = str(n)
        Store.create(s,t)
        return "",201,{"Location":"/posts/"+s} # OK
    else:
        return "",400 # Bad Request


@app.route("/posts/<string:s>",methods=["GET"])
def read(s):
    post = Store.read(s)
    if post != None:
        return post,200 # OK
    else:
        return "",404 # Not Found

@app.route("/posts/<string:s>",methods=["DELETE"])
def delete(s):
    success = Store.delete(s)
    if success:
        return "",200 # OK
    else:
        return "",400 # Not Found

@app.route("/posts",methods=["GET"])
def list():
    ss = Store.list()
    return ss,200 # OK

if __name__ == "__main__":
    app.run(host="localhost",port=3000)
