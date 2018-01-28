from threading import Thread

from flask import Flask, request
from indexer import index_video
import boto3

app = Flask(__name__, static_url_path='')


@app.route("/")
def hello():
    return app.send_static_file('index.html')


@app.route("/process", methods=['POST'])
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
