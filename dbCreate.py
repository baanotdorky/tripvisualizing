import sqlite3


def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS trips (
                    id integer PRIMARY KEY,
                    leaflet_id varchar,
                    name text NOT NULL,
                    latitude_centroid decimal(10),
                    longitude_centroid decimal(10));""")


def delete_table():
    cur.execute("DROP TABLE trips")
    print('Trips table deleted.')


if __name__ == '__main__':
    con = sqlite3.connect("trips.db")

    # See if trip table already exists. If it doesn't, create it.
    cur = con.cursor()
    create_table()
