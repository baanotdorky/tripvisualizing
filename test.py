from Trip import Trip
import os

if __name__ == '__main__':
    for filename in os.scandir('data'):
        if filename.is_file() and filename.path.endswith('.gpx'):
            gpx_file = open(filename.path, 'r')
            temp = Trip(gpx_file, filename.path.replace(' ', '_').replace('\'', ''))
            temp.upload_to_db()
