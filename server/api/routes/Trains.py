from flask import json
from flask_cors import cross_origin

from api.Api import api
import reisapi


@api.route('/api/trains', methods=['GET'])
@cross_origin()
def get_trains():
    response = []
    reisapi.trainLock.acquire()
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
            'lastUpdate': train.lastUpdate.isoformat()
        })
    reisapi.trainLock.release()

    return json.jsonify(
        error=False,
        response=response
    )
