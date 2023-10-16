from Trip import Trip
import dbUtils
import os


def bulk_add_trips():
    """
    Add all gpx files from data subdirectory to SQLite database
    """
    for filename in os.scandir('data'):
        if filename.is_file() and filename.path.endswith('.gpx'):
            add_trip_to_db(filename.path)


def add_trip_to_db(filepath):
    """Add a single trip to the SQL database using a specific filepath"""
    gpx_file = open(filepath, 'r')
    temp = Trip(gpx_file, filepath.replace(' ', '_').replace('\'', ''))
    temp.upload_to_db()


if __name__ == '__main__':
    con, cur = dbUtils.db_connect('trips')
    dbUtils.delete_table('trips', cur)
    dbUtils.create_trips_table(cur)
    bulk_add_trips()
    dbUtils.to_JSON()
