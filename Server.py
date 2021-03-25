from flask import Flask, jsonify, request
from flask_api import status
import base64
import os
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
    print(headers)
    code = status.HTTP_400_BAD_REQUEST
    body = ''
    
    if validate(headers):
        code = status.HTTP_204_NO_CONTENT
        t = threading.Thread(target=worker, args=(request.json,))
        t.start()
    else:
        body = jsonify(status='Authorization header missing or invalid')
    return body, code

def validate(headers):
    status = False
    password = os.environ.get('OKTA_HOOK_PASSWORD')
    if password is not None and 'Authorization' in headers:
        value = headers['Authorization']
        parts = value.split()
        if len(parts) == 2 and parts[0] == 'Basic':
            credentials = 'admin:' + password
            print(parts[1], base64.b64encode(str.encode(credentials)))
            status = str.encode(parts[1]) == base64.b64encode(str.encode(credentials))
    return status

def worker(body):
    print(body)
    # Write it to a GCP bucket - no processing required

app.run(host='0.0.0.0', port=8000)