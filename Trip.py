import pandas as pd
import gpxpy
import folium
import sqlite3
import json


class Trip(object):
    def __init__(self, gpx_file, fname):
        self.gpx_file = gpx_file
        self.fname = fname
        self.gpx = gpxpy.parse(gpx_file)
        self.trip_data = self.set_trip_data()
        self.polyline = self.set_polyline()

    def set_polyline(self):
        """Returns a leaflet PolyLine Object corresponding to the trip

        Returns:
            PolyLine: Leaflet Polyline object for the trip
        """
        return folium.PolyLine(self.trip_data[['latitude', 'longitude']], color='green', weight=4.5, opacity=.5)

    def set_trip_data(self):
        """Parses gpx data and inputs into dataframe with latitude, longitude, elevation, and time columns

        Returns:
            DataFrame: Contains geodata from gpx file (latitude, longitude, elevation, time)
        """
        trip_data = pd.DataFrame()
        for track in self.gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    trip_data = trip_data._append({'latitude': point.latitude,
                                                   'longitude': point.longitude,
                                                   'elevation': point.elevation,
                                                   'time': point.time}, ignore_index=True)
        return trip_data

    def plot_trip(self):
        """Plots trip on a leaflet map and saves to HTML file in current directory (trip_map.html)"""
        trip_map = folium.Map(location=(self.trip_data['latitude'].mean(), self.trip_data['longitude'].mean()),
                              tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
                              attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                                   'contributors &copy;<a href="https://carto.com/attributions">CARTO</a>',
                              )
        self.polyline.add_to(trip_map)
        trip_map.save("trip_map.html")

    def get_mean_latitude(self):
        """Calculates the mean latitude of the trip data

        Returns:
            float: average latitude"""
        return self.trip_data['latitude'].mean()

    def get_mean_longitude(self):
        """Calculates the mean latitude of the trip data

        Returns:
            float: average longitude"""
        return self.trip_data['longitude'].mean()

    def upload_to_db(self):
        """Uploads high-level trip data to trips.db SQL database."""
        con = sqlite3.connect("trips.db")
        cur = con.cursor()
        # Check if trip already exists in db, and return if so
        res = cur.execute("""SELECT * FROM trips WHERE fname={fname}""".format(fname="'"+self.fname+"'"))
        if res.fetchone() is not None:
            return
        cur.execute("""
            INSERT INTO trips(leaflet_id, fname, latitude_centroid, longitude_centroid) VALUES
                ({id}, {fname}, {lat}, {long})
        """.format(id="'"+self.polyline.get_name()+"'", fname="'"+self.fname+"'", lat=self.get_mean_latitude(),
                   long=self.get_mean_longitude()))
        con.commit()
        con.close()
