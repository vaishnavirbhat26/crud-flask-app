from flask import Flask , jsonify, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/favInfo'

mongo = PyMongo(app)

@app.route('/', methods = ['GET'])
def retreiveAll():
    holder = list()
    currentCollection = mongo.db.favInfo
    for i in currentCollection.find():
        holder.append({'name': i['name'], 'genre' : i['favMusic'], 'game' : i['favGame']})
    return jsonify(holder)

@app.route('/<name>', methods = ['GET'])
def retreiveFromName(name):
    currentCollection = mongo.db.favInfo
    data = currentCollection.find_one({"name": name})
    return jsonify({'name': data['name'], 'genre': data['favMusic'], 'game':data['favGame']})
    
@app.route('/postData', methods = ['POST'])
def postData():
    currentCollection = mongo.db.favInfo
    name = request.json['name']
    genre = request.json['genre']
    game = request.json['game']
    currentCollection.insert_one({'name' : name, 'favMusic': genre, 'favGame': game})
    return jsonify({'name' : name, 'genre': genre, 'game':game})

@app.route('/deleteData/<name>', methods = ['DELETE'])
def deleteData(name):
    currentCollection = mongo.db.favInfo
    currentCollection.delete_one({'name':name})
    return redirect(url_for('retreiveAll'))

@app.route('/update/<name>', methods = ['PUT'])
def updateData(name):
    currentCollection = mongo.db.favInfo
    updatedName = request.json['name']
    currentCollection.update_one({'name': name},{"$set": {'name' : updatedName}})
    return redirect(url_for('retreiveAll'))


if __name__ == '__main__':
    app.run(debug=True)