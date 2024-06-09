from flask import Flask, render_template, request, jsonify, Response
import json
import os
from functools import wraps

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
DATABASE_FILE = 'database.json'
USER = os.getenv("USER", "test")
PASSWORD = os.getenv("PASSWORD", "test")

def read_data():
    try:
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return ""

def write_data(data):
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f)

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
