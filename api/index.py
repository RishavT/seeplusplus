from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'database.json')

def read_data():
    try:
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return ""

def write_data(data):
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/load', methods=['GET'])
def load():
    data = read_data()
    return render_template('clipboard.html', text=data)

@app.route('/save', methods=['POST'])
def save():
    data = request.form.get('text', '')
    write_data(data)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

if __name__ != "__main__":
    # Make sure the serverless function is picked up by Vercel
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    from werkzeug.serving import run_simple
    app = DispatcherMiddleware(app)
