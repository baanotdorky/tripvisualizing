import gpxpy
import pandas as pd
import folium
import webbrowser

if __name__ == '__main__':
    gpx_file = open('data/Morning hike at High Divide and Seven Lakes Basin Loop.gpx', 'r')
    gpx = gpxpy.parse(gpx_file)
    trip = pd.DataFrame()
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                trip = trip._append({'latitude': point.latitude,
                                     'longitude': point.longitude,
                                     'elevation': point.elevation,
                                     'time': point.time}, ignore_index=True)
    print(trip)
    trip_map = folium.Map(location=(trip['latitude'].mean(), trip['longitude'].mean()),
                          tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
                          attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                               'contributors &copy;<a href="https://carto.com/attributions">CARTO</a>',
                          )
    folium.PolyLine(trip[['latitude', 'longitude']], color='green', weight=4.5, opacity=.5).add_to(trip_map)
    trip_map.save("trip_map.html")
    webbrowser.open("trip_map.html")
