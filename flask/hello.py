from flask import Flask
from flask import url_for

app = Flask(__name__)


from flask import render_template


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("hello/hello.html", name=name)
