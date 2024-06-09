from flask import Flask, render_template, request, jsonify, Response
import json
import os
from functools import wraps

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))

INMEM_DB = ""
USER = os.getenv("USER", "test")
PASSWORD = os.getenv("PASSWORD", "test")

def read_data():
    return INMEM_DB

def write_data(data):
    global INMEM_DB
    if data != INMEM_DB:
        INMEM_DB = data

def check_auth(username, password):
    return username == USER and password == PASSWORD

def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
@requires_auth
def load():
    data = read_data()
    return render_template('clipboard.html', text=data)

@app.route('/save', methods=['POST'])
@requires_auth
def save():
    data = request.form.get('text', '')
    write_data(data)
    return jsonify({'status': 'success'})
