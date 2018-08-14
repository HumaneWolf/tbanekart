from datetime import datetime
from dateutil.parser import parse
import requests
import utm
from urllib3.exceptions import MaxRetryError

from lib.Config import Config
from lib import Logger
import reisapi
from reisapi.Train import Train


class Station:
    def __init__(self, station):
        self.station = station['ID']

        self.name = station['Name']

        position = utm.to_latlon(station['X'], station['Y'], 32, 'X')
        self.lat = position[0]
        self.lon = position[1]

        self.lastUpdate = datetime(1970, 1, 1)

        Logger.info('New stop ' + self.name + ' has been loaded ' + str(position) + '.')

    def get_departures(self):
        # Logger.info('Request: ' + str(self.station))
        try:
            r = requests.get(Config['REISAPI']['base'] + 'StopVisit/GetDepartures/' + str(self.station))
        except (MaxRetryError, TimeoutError, ConnectionError) as e:
            Logger.warn("Ruter API returned exception: " + e)
            return []
        if r.status_code != 200:
            Logger.warn("Ruter API returned status " + str(r.status_code))
            return []
        return r.json()

    def update_trains(self):
        self.lastUpdate = datetime.utcnow()

        departures = self.get_departures()

        for departure in departures:
            if departure['MonitoredVehicleJourney']['VehicleRef'] is None \
                    or departure['MonitoredVehicleJourney']['VehicleRef'] == 'null':
                break

            local_dep = parse(departure['MonitoredVehicleJourney']['MonitoredCall']['ExpectedDepartureTime'])
            departure_time = datetime(
                local_dep.year,
                local_dep.month,
                local_dep.day,
                local_dep.hour,
                local_dep.minute,
                local_dep.second,
                local_dep.microsecond
            ) - local_dep.utcoffset()

            if departure['MonitoredVehicleJourney']['VehicleRef'] not in reisapi.trains:
                reisapi.trainLock.acquire()
                reisapi.trains[departure['MonitoredVehicleJourney']['VehicleRef']] = \
                    Train(departure['MonitoredVehicleJourney']['VehicleRef'])
                reisapi.trainLock.release()

                reisapi.trains[departure['MonitoredVehicleJourney']['VehicleRef']].set_line(
                    departure['MonitoredVehicleJourney']['LineRef'],
                    departure['MonitoredVehicleJourney']['DestinationName']
                )
                reisapi.trains[departure['MonitoredVehicleJourney']['VehicleRef']].add_station(
                    self,
                    departure_time,
                    departure['MonitoredVehicleJourney']['LineRef'],
                    departure['MonitoredVehicleJourney']['DestinationName']
                )
            else:
                train = reisapi.trains[departure['MonitoredVehicleJourney']['VehicleRef']]

                reisapi.trains[departure['MonitoredVehicleJourney']['VehicleRef']].add_station(
                    self,
                    departure_time,
                    departure['MonitoredVehicleJourney']['LineRef'],
                    departure['MonitoredVehicleJourney']['DestinationName']
                )

                if departure_time < train.nextStationDep:
                    train.set_line(
                        departure['MonitoredVehicleJourney']['LineRef'],
                        departure['MonitoredVehicleJourney']['DestinationName']
                    )
