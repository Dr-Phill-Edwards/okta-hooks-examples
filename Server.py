from flask import Flask, jsonify, request
from flask_api import status
import threading

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handleGet():
    headers = dict(request.headers)
    if 'X-Okta-Verification-Challenge' in headers:
        value = headers['X-Okta-Verification-Challenge']
        code = status.HTTP_200_OK
        body =  jsonify(verification=value)
    else:
        code = status.HTTP_400_BAD_REQUEST
        body = jsonify(status='Verification header missing')
    return body, code

@app.route('/', methods=['POST'])
def handlePost():
    headers = dict(request.headers)
    t = threading.Thread(target=worker, args=(request.json,))
    t.start()
    return '', status.HTTP_201_CREATED

def worker(body):
    print(body)
    # Write it to a GCP bucket - no processing required

app.run(host='0.0.0.0', port=8000)