from flask import Flask, render_template, request, jsonify, Response
import json
import os
from functools import wraps
from encrypt import encrypt, decrypt

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))

INMEM_DB = {}
SUPPORTED_USER_COUNT = 2
USERS = [
    {
        "user": "test",
        "password": "test",
    }
]

for i in range(1, SUPPORTED_USER_COUNT + 1):
    USERS.append({"user": os.getenv(f"USER{i}", f"test{i}"), "password": os.getenv(f"PASSWORD{i}", f"test{i}")})


def read_data(identity):
    encrypted = INMEM_DB.get(identity["user"])

    if not encrypted:
        return ""

    return decrypt(
        enc_text=encrypted,
        passphrase=identity["password"],
    )


def write_data(data, identity):
    global INMEM_DB

    if not data:
        INMEM_DB[identity["user"]] = ""
        return

    encrypted = encrypt(
        text=data,
        passphrase=identity["password"],
    )

    INMEM_DB[identity["user"]] = encrypted

def authenticate(logout=False):
    if logout:
        return Response(
            response=render_template("logout.html"),
            status=401
        )

    return Response(
        "Could not verify your access level for that URL.\n"
        "You have to login with proper credentials",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


def get_identity():
    auth = request.authorization
    for identity in USERS:
        user = identity["user"]
        password = identity["password"]
        if auth and user == auth.username and password == auth.password:
            return identity


@app.route("/", methods=["GET"])
def load():
    identity = get_identity()
    if not identity:
        return authenticate()

    data = read_data(identity=identity)
    return render_template("clipboard.html", text=data, user=identity["user"])


@app.route("/save", methods=["POST"])
def save():
    identity = get_identity()
    if not identity:
        return authenticate()

    data = request.form.get("text", "")
    write_data(data, identity=identity)
    return jsonify({"status": "success"})

@app.route("/logout")
def logout():
    return authenticate(logout=True)
