from flask import json
from flask_cors import cross_origin

from api.Api import api
import reisapi


@api.route('/api/trains', methods=['GET'])
@cross_origin()
def get_trains():
    return json.jsonify(
        error=False,
        response=reisapi.trainsCache
    )
