from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost/blogposts"
mongo = PyMongo(app)
db = mongo.db.blogposts

CORS(app)

# Routes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


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
    return render_template('blogposts.html', posts=posts)


@app.route('/blogposts/create_blogpost', methods=['GET'])
def create_blogpost():
    return render_template('create.html')


@app.route('/blogposts/create', methods=['POST'])
def create_blog():
    title = request.form['title']
    text = request.form['text']
    date = request.form['date']

    if request.method == 'POST':
        db.insert_one({
            'title': title,
            'text': text,
            'date': date
        })

        return redirect(url_for('blogposts'))


@app.route('/blogposts/<id>', methods=['GET'])
def get_blog(id):
    post = db.find_one({'_id': ObjectId(id)})
    return render_template('post.html', post=post)


@app.route('/blogposts/update_post/<id>', methods=['GET'])
def update_post(id):
    post = db.find_one({'_id': ObjectId(id)})
    return render_template('update.html', post=post)


@app.route('/blogposts/update/<id>', methods=['POST'])
def update_blog(id):
    title = request.form['title']
    text = request.form['text']
    date = request.form['date']

    if request.method == "POST":
        db.update_one({'_id': ObjectId(id)}, {'$set': {
            'title': title,
            'text': text,
            'date': date
        }})

        return redirect(url_for('blogposts'))


@app.route('/blogposts/delete/<id>', methods=['POST'])
def delete_blog(id):
    if request.method == "POST":
        db.remove({'_id': ObjectId(id)})
        return redirect(url_for('blogposts'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)
