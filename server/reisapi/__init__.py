from datetime import datetime, timedelta
from gevent import Greenlet, sleep
import requests
from threading import Thread, RLock

from lib.Config import Config
from reisapi.Station import Station

stations = {}
trains = {}
trainLock = RLock()

trainsCache = []


def run():
    # Load station list
    routes = Config['REISAPI']['metroLines'].split(',')
    for route in routes:
        r = requests.get(Config['REISAPI']['base'] + 'Line/GetStopsByLineId/' + route)
        if r.status_code != 200:
            return []
        json = r.json()
        for station in json:
            if station['ID'] in stations:
                continue
            stations[station['ID']] = Station(station)

    # Update loop
    while True:
        # Update stations
        stations_by_last_update = []
        for s in (sorted(stations.keys(), key=lambda identifier: stations[identifier].lastUpdate)):
            stations_by_last_update.append(s)

        update_counter = 0  # Used to make sure we spread the station updates out.
        for station in stations_by_last_update:
            g = Greenlet(stations[station].update_trains())  # Async, let it run in a greenlet.
            g.start()
            update_counter = update_counter + 1
            # Stop us from running all at once, effectively spreading them out.
            if update_counter > int(Config['REISAPI']['updateFrequency']):
                break

        # Update trains
        deletion_queue = []
        trainLock.acquire()
        for train in trains.values():
            if train.lastUpdate < (datetime.utcnow() - timedelta(minutes=5)):
                deletion_queue.append(train.train)
            else:
                train.update_position()
        for train in deletion_queue:
            del trains[train]

        trainsCache.clear()
        for train in trains.values():
            if train.nextStation is not None:
                next_stop_name = train.nextStation.name
            else:
                next_stop_name = 'Loading..'
            if train.prevStation is not None:
                prev_stop_name = train.prevStation.name
            else:
                prev_stop_name = 'Loading..'
            trainsCache.append({
                'id': train.train,
                'line': train.line,
                'destination': train.destination,
                'nextStop': {
                    'name': next_stop_name,
                    'time': train.nextStationDep.isoformat()
                },
                'prevStop': {
                    'name': prev_stop_name,
                    'time': train.prevStationDep.isoformat()
                },
                'lat': train.lat,
                'lon': train.lon,
                'lastUpdate': train.lastUpdate.isoformat()
            })
        trainLock.release()

        # Delay next loop.
        sleep(float(Config['REISAPI']['sleepTime']))


class ReisThread(Thread):
    def run(self):
        run()
