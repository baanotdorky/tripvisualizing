import pandas as pd
import gpxpy
import folium


class Trip(object):
    def __init__(self, gpx_file):
        self.gpx_file = gpx_file
        self.gpx = gpxpy.parse(gpx_file)
        self.trip_data = self.set_trip_data()

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
        (folium.PolyLine(self.trip_data[['latitude', 'longitude']], color='green', weight=4.5, opacity=.5)
         .add_to(trip_map))
        trip_map.save("trip_map.html")
