from flask import Flask, render_template, request, session, redirect, Response
from datetime import datetime, timedelta
from pymongo import MongoClient
from http import HTTPStatus

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.permanent_session_lifetime = timedelta(minutes=1)

client = MongoClient("mongodb://localhost:27017/")
db = client["todolist"]
users_collection = db["todocollection"]

def is_valid_username(username):
    if not username.isalnum():
        return False

    if not 6 <= len(username) <= 12:
        return False

    return True

def is_valid_password(password):
    if len(password) < 6:
        return False

    return True

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
            error_message = 'Invalid credentials.'
            return Response(error_message, status=HTTPStatus.UNAUTHORIZED)

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
            error_message = 'Username already exists.'
            return Response(error_message, status=HTTPStatus.BAD_REQUEST)
        else:
            if not is_valid_username(username):
                error_message = 'Invalid username. Username should be alphanumeric and between 6-12 characters.'
                return Response(error_message, status=HTTPStatus.BAD_REQUEST)
            elif not is_valid_password(password):
                error_message = 'Invalid password. Password should be at least 6 characters long.'
                return Response(error_message, status=HTTPStatus.BAD_REQUEST)
            else:
                user = {"username": username, "password": password, "role": role}
                users_collection.insert_one(user)
                return redirect('/')

    return render_template('add_user.html')

if __name__ == '__main__':
    app.run(debug=True)
