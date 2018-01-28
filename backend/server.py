from threading import Thread

from flask import Flask, request
from indexer import index_video
import boto3

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/process")
def process():
    if request.method == 'POST':
        client = boto3.client("dynamodb")
        res = client.get_item(
            TableName='index',
            Key={
                'url': {
                    'S': request.form['url']
                }
            }
        )
        if 'Item' in res:
            return "Already Exists"
        background_thread = Thread(target=index_video, args=(request.form['url'],))
        background_thread.start()
        return "Processing"
