from datetime import datetime
from threading import RLock


class StationVisit:
    def __init__(self, station, time):
        self.station = station
        self.time = time


class Train:
    def __init__(self, train):
        self.train = train

        self.lastUpdate = datetime.utcnow()

        self.visitLock = RLock()
        self.stationVisits = {}

        self.nextStation = None
        self.nextStationDep = datetime(1970, 1, 1)
        self.prevStation = None
        self.prevStationDep = datetime(1970, 1, 1)

        self.lat = 0
        self.lon = 0

        self.line = 0
        self.destination = ''

    def set_line(self, line, destination):
        self.lastUpdate = datetime.utcnow()

        self.line = line
        self.destination = destination

    def add_station(self, station, time, line, destination):
        self.lastUpdate = datetime.utcnow()

        self.visitLock.acquire()
        if (str(station.station) + line + destination) not in self.stationVisits:
            self.stationVisits[str(station.station) + line + destination] = StationVisit(station, time)
        else:
            self.stationVisits[str(station.station) + line + destination].time = time
        self.visitLock.release()

    def update_position(self):
        self.visitLock.acquire()
        now = datetime.utcnow()
        stop = StationVisit(self.nextStation, self.nextStationDep)
        for visit in self.stationVisits.values():
            if stop.station is None:
                stop = visit
            else:
                if now < visit.time and (visit.time < stop.time or stop.time < now):
                    stop = visit
        self.nextStation = stop.station
        self.nextStationDep = stop.time

        stop = StationVisit(self.prevStation, self.prevStationDep)
        for visit in self.stationVisits.values():
            if stop.station is None:
                if now > visit.time:
                    stop = visit
            else:
                if now > visit.time and visit.time > stop.time:
                    stop = visit
        self.prevStation = stop.station
        self.prevStationDep = stop.time

        deletion = []
        for key, visit in self.stationVisits.items():
            if visit.time < now:
                deletion.append(key)
        for stop in deletion:
            del self.stationVisits[stop]
        self.visitLock.release()

        if self.prevStation is None or self.nextStation is None:
            return  # Can't update it yet.
        if self.prevStation is self.nextStation:
            return  # Still not enough info to update.

        travel_time = self.nextStationDep - self.prevStationDep
        travel_to_next = self.nextStationDep - datetime.utcnow()
        travel_from_prev = datetime.utcnow() - self.prevStationDep

        part_weight = travel_time.total_seconds() / 2
        next_weight = travel_from_prev.total_seconds() / part_weight
        prev_weight = travel_to_next.total_seconds() / part_weight

        self.lat = ((self.nextStation.lat * next_weight) + (self.prevStation.lat * prev_weight)) / 2
        self.lon = ((self.nextStation.lon * next_weight) + (self.prevStation.lon * prev_weight)) / 2

        # self.lat = (self.nextStation.lat + self.prevStation.lat) / 2
        # self.lon = (self.nextStation.lon + self.prevStation.lon) / 2
