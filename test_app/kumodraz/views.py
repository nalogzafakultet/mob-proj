from kumodraz import app
from flask import request, jsonify


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "OK",
        "result": {
            "method": "GET",
            "url": {},
            "body": {}
        }
    })

