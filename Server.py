from flask import Flask, jsonify, request
from flask_api import status

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle():
    headers = dict(request.headers)
    print(headers)
    if 'X-Okta-Verification-Challenge' in headers:
        value = headers['X-Okta-Verification-Challenge']
        code = status.HTTP_200_OK
        body =  jsonify(verification=value)
    else:
        code = status.HTTP_400_BAD_REQUEST
        body = jsonify(status='Verification header missing')
    return body, code

app.run(host='0.0.0.0', port=8000)