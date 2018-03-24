from flask import json
from flask_cors import cross_origin

from api.Api import api


@api.route('/api/ping', methods=['GET'])
@cross_origin()
def get_ping():
    return json.jsonify(
        error=False,
        response='Pong!'
    )
