from flask import json

from api.Api import api
import reisapi


@api.route('/api/trains', methods=['GET'])
def get_trains():
    response = []
    for train in reisapi.trains.values():
        response.append({
            'id': train.train,
            'line': train.line,
            'destination': train.destination,
            'nextStop': {
                'name': train.nextStation.name,
                'time': train.nextStationDep.isoformat()
            },
            'lat': train.lat,
            'lon': train.lon,
            'lastUpdate': train.lastUpdate
        })

    return json.jsonify(
        error=False,
        response=response
    )
