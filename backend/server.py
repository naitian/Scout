from threading import Thread

from flask import Flask, request
from indexer import index_video

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/process")
def process():
    if request.method == 'POST':
        background_thread = Thread(target=index_video, args=(request.form['url'],))
        background_thread.start()
        return "Processing"
