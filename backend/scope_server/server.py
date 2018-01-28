from flask import Flask, request
from ..indexer import index_video

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/process")
def process():
    if request.method == 'POST':
        index_video(request.form['url'])
