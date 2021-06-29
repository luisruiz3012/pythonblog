from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost/blogposts"
mongo = PyMongo(app)
db = mongo.db.blogposts

CORS(app)

# Routes


@app.route('/blogposts', methods=['GET'])
def blogposts():
    posts = []
    for post in db.find():
        posts.append({
            '_id': str(ObjectId(post['_id'])),
            'title': post['title'],
            'text': post['text'],
            'date': post['date']
        })
    return jsonify({'posts': posts})


@app.route('/blogposts/create', methods=['POST'])
def create_blog():
    title = request.json['title']
    text = request.json['text']
    date = request.json['date']

    db.insert_one({
        'title': title,
        'text': text,
        'date': date
    })

    return jsonify({'Message': 'Post created successfully'})


@app.route('/blogposts/<id>', methods=['GET'])
def get_blog(id):
    post = db.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(id)),
        'title': post['title'],
        'text': post['text'],
        'date': post['date']
    })


@app.route('/blogposts/update/<id>', methods=['PUT'])
def update_blog(id):
    title = request.json['title']
    text = request.json['text']
    date = request.json['date']

    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'title': title,
        'text': text,
        'date': date
    }})

    return jsonify({'Message': 'Post updated successfully'})


@app.route('/blogposts/delete/<id>', methods=['DELETE'])
def delete_blog(id):
    db.remove({'_id': ObjectId(id)})
    return jsonify({'Message': 'Post deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True, port=4000)
