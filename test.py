from Trip import Trip
from TripBook import TripBook
import os

if __name__ == '__main__':
    kodys_trips = TripBook("Kody's Trips")
    for filename in os.scandir('data'):
        if filename.is_file() and filename.path.endswith('.gpx'):
            gpx_file = open(filename.path, 'r')
            kodys_trips.add_trip(Trip(gpx_file, filename.path))
    kodys_trips.plot_trips()

