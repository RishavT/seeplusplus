from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

DATABASE_FILE = 'database.json'

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
