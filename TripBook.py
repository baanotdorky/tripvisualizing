import pandas as pd
import gpxpy
import folium

from tripvisualizing.Trip import Trip


class TripBook(object):
    def __init__(self, name):
        self.name = name
        self.trips = {}

    def add_trip(self, trip: Trip):
        """Add a Trip object to the TripBook trips dictionary"""
        self.trips[trip.fname] = trip

    def plot_trips(self):
        """Plots all trips in the trips dictionary on a leaflet map and saves to HTML file in current directory (
        trip_map.html)"""
        trip_map = folium.Map(location=(47.947711834842806, -123.7691920),
                              tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
                              attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                                   'contributors &copy;<a href="https://carto.com/attributions">CARTO</a>',
                              )
        for trip in self.trips.keys():
            self.trips[trip].polyline.add_to(trip_map)
        trip_map.save("trip_map.html")
