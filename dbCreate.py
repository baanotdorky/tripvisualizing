import sqlite3
import json

def create_table():
    """Creates trips database in SQLite server, if it does not already exist."""
    cur.execute("""CREATE TABLE IF NOT EXISTS trips (
                    id integer PRIMARY KEY,
                    leaflet_id varchar,
                    fname text NOT NULL,
                    name text,
                    latitude_centroid decimal(10),
                    longitude_centroid decimal(10));""")


def delete_table():
    """Deletes trips table from SQLite server."""
    cur.execute("DROP TABLE trips")
    print('Trips table deleted.')

def to_JSON( json_str = True ):
    """Converts entire trips database to JSON and saves to JSON directory: JSON/trips.json"""
    conn = sqlite3.connect('trips.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()

    rows = db.execute('''
    SELECT * from trips
    ''').fetchall()

    conn.commit()
    conn.close()

    json_data = json.dumps([dict(ix) for ix in rows])
    with open('website/JSON/trips.json', 'w') as outfile:
        outfile.write(json_data)



if __name__ == '__main__':
    #con = sqlite3.connect("trips.db")

    # See if trip table already exists. If it doesn't, create it.
    #cur = con.cursor()
    #create_table()
    #delete_table()
    to_JSON()

