import sqlite3
import json


def create_trips_table(cur):
    """Creates trips database in SQLite server, if it does not already exist."""
    cur.execute("""CREATE TABLE IF NOT EXISTS trips (
                    id integer PRIMARY KEY,
                    fname text NOT NULL,
                    name text,
                    latitude_centroid decimal(10),
                    longitude_centroid decimal(10),
                    latlng varchar);""")


def db_connect(db_name):
    con = sqlite3.connect(db_name + ".db")
    cur = con.cursor()
    return con, cur


def delete_table(table_name, cur):
    """Deletes trips table from SQLite server."""
    cur.execute("DROP TABLE {table}".format(table=table_name))
    print('Trips table deleted.')


def to_JSON():
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
    con, cur = db_connect('trips')
    create_trips_table()
    # delete_table('trips')
    to_JSON()
