from datetime import datetime


class Train:
    def __init__(self, train):
        self.train = train

        self.lastUpdate = datetime.utcnow()

        self.nextStation = None
        self.nextStationDep = datetime.utcnow()
        self.prevStation = None
        self.prevStationDep = datetime.utcnow()

        self.lat = 0
        self.lon = 0

        self.line = 0
        self.destination = ''

    def set_line(self, line, destination):
        self.lastUpdate = datetime.utcnow()

        self.line = line
        self.destination = destination

    def set_next_station(self, station, time):
        self.lastUpdate = datetime.utcnow()

        self.prevStation = self.nextStation
        self.prevStationDep = self.nextStationDep
        self.nextStation = station
        self.nextStationDep = time

    def update_position(self):
        if self.prevStation is None or self.nextStation is None:
            return  # Can't update it yet.

        travel_time = self.nextStationDep - self.prevStationDep
        travel_to_next = self.nextStationDep - datetime.utcnow()
        travel_from_prev = datetime.utcnow() - self.prevStationDep

        total_weight = travel_time.total_seconds()
        next_weight = travel_from_prev.total_seconds() / (total_weight / 2)
        prev_weight = travel_to_next.total_seconds() / (total_weight / 2)

        # print('n: ' + str(next_weight) + ' p: ' + str(prev_weight))
        next_weight = 1
        prev_weight = 1

        self.lat = ((self.nextStation.lat * next_weight) + (self.prevStation.lat * prev_weight)) / 2
        self.lon = ((self.nextStation.lon * next_weight) + (self.prevStation.lon * prev_weight)) / 2
