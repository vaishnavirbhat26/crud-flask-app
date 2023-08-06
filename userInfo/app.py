from flask import Flask , jsonify, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/userInfo'

mongo = PyMongo(app)

@app.route('/users', methods = ['GET'])
def retreiveAll():
    holder = list()
    currentCollection = mongo.db.userInfo
    for i in currentCollection.find():
        holder.append({'name': i['name'], 'email' : i['email']})
    return jsonify(holder)

@app.route('/users/<id>', methods = ['GET'])
def retreiveFromName(id):
    currentCollection = mongo.db.userInfo
    data = currentCollection.find_one({"userId": id})
    return jsonify({'id':data['id'],'name': data['name'], 'email': data['email']})
 
@app.route('/postData', methods = ['POST'])
def postData():
    currentCollection = mongo.db.userInfo
    id = request.json['id']
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    currentCollection.insert_one({'id' : id,'name' : name, 'email': email, 'password': password})
    return jsonify({'id' : id,'name' : name, 'email': email, 'password':password})

@app.route('/deleteData/<id>', methods = ['DELETE'])
def deleteData(id):
    currentCollection = mongo.db.userInfo
    currentCollection.delete_one({'id':id})
    return redirect(url_for('retreiveAll'))

@app.route('/update/<id>', methods = ['PUT'])
def updateData(id):
    currentCollection = mongo.db.userInfo
    updatedName = request.json['id']
    currentCollection.update_one({'id': id},{"$set": {'id' : updatedName}})
    return redirect(url_for('retreiveAll'))


if __name__ == '__main__':
    app.run(debug=True)