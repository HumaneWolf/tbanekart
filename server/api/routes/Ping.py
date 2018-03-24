from flask import json

from api.Api import api


@api.route('/api/ping', methods=['GET'])
def get_ping():
    return json.jsonify(
        error=False,
        response='Pong!'
    )
