from flask import json, make_response
from flask_cors import cross_origin

from api.Api import api, redis


@api.route('/api/stations', methods=['GET'])
@cross_origin()
def get_stations():
    if redis.exists('tbane:stations'):
        resp = make_response(redis.get('tbane:stations'), 200)
        resp.headers['Content-Type'] = 'application/json'
        return resp
    else:
        return json.jsonify(
            error=False,
            response=[]
        )
