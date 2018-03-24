from flask import json

from api.Api import api
import reisapi


@api.route('/api/stations', methods=['GET'])
def get_stations():
    response = []
    for station in reisapi.stations.values():
        response.append({
            'id': station.station,
            'name': station.name,
            'lat': station.lat,
            'lon': station.lon
        })

    return json.jsonify(
        error=False,
        response=response
    )
