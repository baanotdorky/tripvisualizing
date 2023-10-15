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
                                                   'latlng': [point.latitude, point.longitude]}
                                                   , ignore_index=True)
        return trip_data

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

    def upload_to_db(self, verbose=True):
        """Uploads high-level trip data to trips.db SQL database."""
        con = sqlite3.connect("trips.db")
        cur = con.cursor()
        if verbose==True:
            print('Adding gpx data to database: ' + self.fname)
        # Check if trip already exists in db, and return if so
        res = cur.execute("""SELECT * FROM trips WHERE fname={fname}""".format(fname="'"+self.fname+"'"))
        if res.fetchone() is not None:
            return
        cur.execute("""
            INSERT INTO trips(fname, name, latitude_centroid, longitude_centroid, latlng) VALUES
                ({fname}, {name},{lat}, {long}, {latlng})
        """.format(fname="'"+self.fname+"'",
                   name="'"+self.fname.split('.gpx')[0].split('/')[1].replace('_',' ')+"'", lat=self.get_mean_latitude(),
                   long=self.get_mean_longitude(),
                   latlng="'"+str(self.trip_data['latlng'].tolist())+"'"))
        con.commit()
        con.close()
