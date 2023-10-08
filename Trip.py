import pandas as pd
import gpxpy
import folium
import sqlite3
import json


class Trip(object):
    def __init__(self, gpx_file, name):
        self.gpx_file = gpx_file
        self.name = name
        self.gpx = gpxpy.parse(gpx_file)
        self.trip_data = self.set_trip_data()
        self.polyline = self.set_polyline()

    def set_polyline(self):
        return folium.PolyLine(self.trip_data[['latitude', 'longitude']], color='green', weight=4.5, opacity=.5)

    def set_trip_data(self):
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
        trip_map = folium.Map(location=(self.trip_data['latitude'].mean(), self.trip_data['longitude'].mean()),
                              tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
                              attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                                   'contributors &copy;<a href="https://carto.com/attributions">CARTO</a>',
                              )
        self.polyline.add_to(trip_map)
        trip_map.save("trip_map.html")

    def get_mean_latitude(self):
        return self.trip_data['latitude'].mean()

    def get_mean_longitude(self):
        return self.trip_data['longitude'].mean()

    def upload_to_db(self):
        con = sqlite3.connect("trips.db")
        cur = con.cursor()
        # Check if trip already exists in db, and return if so
        res = cur.execute("""SELECT * FROM trips WHERE name={name}""".format(name="'"+self.name+"'"))
        if res.fetchone() is not None:
            return
        cur.execute("""
            INSERT INTO trips(leaflet_id, name, latitude_centroid, longitude_centroid) VALUES
                ({fname}, {name}, {lat}, {long})
        """.format(fname="'"+self.polyline.get_name()+"'", name="'"+self.name+"'", lat=self.get_mean_latitude(),
                   long=self.get_mean_longitude()))
        con.commit()
        con.close()
