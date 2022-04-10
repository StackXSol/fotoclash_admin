from flask import Flask, jsonify,render_template, request, json
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
    id = eval(id['id'])
    value = id['id']
    db.collection('Withdrawls').document(value).update({'Status': True})
    return jsonify({"res": "Success"})

@app.route("/sendfalse", methods=["POST", "GET"])
def sendfalse():
    id = request.get_json('id')
    id = eval(id['id'])
    value = id['id']
    db.collection('Withdrawls').document(value).update({'Status': False})
    return jsonify({"res": "Success"})