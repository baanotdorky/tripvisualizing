import gpxpy

if __name__ == '__main__':
    gpx_file = open('data/Morning hike at High Divide and Seven Lakes Basin Loop.gpx', 'r')
    gpx = gpxpy.parse(gpx_file)
    print(gpx.tracks[0].segments[0].points)