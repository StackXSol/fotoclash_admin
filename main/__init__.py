import hashlib
from flask import Flask, jsonify,render_template, request,  redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('main/db.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"


@app.route("/")
def Login():
    return render_template("login.html")

@app.route('/validate', methods=['POST','GET'])
def validate():
    username = request.form['username']
    password = request.form['password']
    md5 = hashlib.md5(password.encode('utf8'))
    user = db.collection("Admin").get()
    if user:
        dbpass=""
        for item in user:
            if item.to_dict()['Email'] == username:
                dbpass = item.to_dict()['Password']
        if dbpass:
            if dbpass == (md5.hexdigest().upper()):
                return redirect(url_for("Home"))
    return redirect(url_for("Login"))


@app.route("/home")
def Home():
    response = db.collection("Withdrawls").get()
    data = []
    for item in response:
        print(item)
        data.append(item.to_dict())
    return render_template("home.html", data=data)

@app.route("/sendtrue", methods=["POST", "GET"])
def sendtrue():
    id = request.get_json('id')
    value = id['id']
    data = db.collection('Users').document(value).stream()
    data = data.to_dict()
    # for i in data:
    #     if i == "Wallet":
    #         for j in i:
    #             print(j)
    #         break
    print(data)
    # db.collection('Users').document(value).update({"Pending": })
    res = db.collection('Withdrawls').where("UserID","==",str(value)).stream()
    print(res)
    for i in res:
        i.reference.update({"Status": True}) 
    return jsonify({"res": "Success"})

@app.route("/sendfalse", methods=["POST", "GET"])
def sendfalse():
    id = request.get_json('id')
    print(id)
    value = id['id']
    res = db.collection('Withdrawls').where("UserID","==",str(value)).stream()
    print(res)
    for i in res:
        i.reference.update({"Status": False}) 
    return jsonify({"res": "Success"})


@app.route('/getdata', methods=["POST","GET"])
def getdata():
    print("Get Data")
    response = db.collection('Withdrawls').where("Status","==",True).get()
    data = []
    for item in response:
        print(item.to_dict())
        data.append(item.to_dict())
    return jsonify({"res":data})
