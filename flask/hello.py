from flask import Flask

app = Flask(__name__)

from markupsafe import escape


@app.route("/")
def index():
    return "Index Page"


@app.route("/hello")
def hello():
    return "Hello, World"
