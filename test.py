from Trip import Trip

if __name__ == '__main__':
    gpx_file = open('data/Morning hike at High Divide and Seven Lakes Basin Loop.gpx', 'r')
    high_divide = Trip(gpx_file)
    high_divide.plot_trip()

