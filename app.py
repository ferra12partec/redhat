import json
from flask import Flask, jsonify, request
from spacy_model import predict

application = Flask(__name__)


@application.route('/')
@application.route('/status')
def status():
    return jsonify({'status': 'ok'})


@application.route('/predictions', methods=['GET','POST'])
def create_prediction():
    data = request.data or '{}'
    body = json.loads(data)
    return jsonify(predict(body))

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=8080) # Launch built-in we server and run this Flask webapp