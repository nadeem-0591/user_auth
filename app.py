from flask import Flask, render_template, request, session, redirect, flash
from datetime import datetime, timedelta
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.permanent_session_lifetime = timedelta(minutes=1)

client = MongoClient("mongodb://localhost:27017/")
db = client["todolist"]
users_collection = db["todocollection"]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({"username": username, "password": password})

        if user:
            session['username'] = user['username']
            session['last_activity'] = datetime.now()
            return redirect('/home')
        else:
            print('Invalid credentials.')

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        session['last_activity'] = datetime.now()
        return render_template('home.html', username=session['username'])
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            print('Username already exists.')
        else:
            user = {"username": username, "password": password, "role": role}
            users_collection.insert_one(user)
            print('User created successfully.')

        return redirect('/')

    return render_template('add_user.html')

if __name__ == '__main__':
    app.run(debug=True)