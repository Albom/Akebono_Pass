import sqlite3
import glob
from file_formats import load_data, load_orbits


class Database:

    def __init__(self):
        self.conn = None

    def connect(self, filename):
        # if not os.path.isfile(file_name):
        #     return False
        # if self.conn is not None:
        #     self.conn.close()
        self.conn = sqlite3.connect(filename)
        return True

    def close(self):
        self.conn.close()

    def create_data_table(self):
        q = """
            CREATE TABLE data (
            id INTEGER PRIMARY KEY,
            date VARCHAR(20),
            altitude DOUBLE,
            mlt DOUBLE,
            l_value DOUBLE,
            ne DOUBLE
            );
            """
        cur = self.conn.cursor()
        try:
            cur.execute(q)
        except sqlite3.Error as err:
            print(err)

    def insert_data(self, date, altitude, mlt, l_value, ne):
        q = f"""
        INSERT INTO data
        (date, altitude, mlt, l_value, ne)
        VALUES ('{date}', {altitude}, {mlt}, {l_value}, {ne});
        """
        cur = self.conn.cursor()
        try:
            cur.execute(q)
            cur.close()
        except sqlite3.Error as err:
            print(err)

    def create_orbits_table(self):
        q = """
            CREATE TABLE orbits (
            id INTEGER PRIMARY KEY,
            date VARCHAR(20),
            altitude DOUBLE,
            lat DOUBLE,
            lon DOUBLE
            );
            """
        cur = self.conn.cursor()
        try:
            cur.execute(q)
        except sqlite3.Error as err:
            print(err)

    def insert_orbits(self, date, altitude, lat, lon):
        q = f"""
        INSERT INTO orbits
        (date, altitude, lat, lon)
        VALUES ('{date}', {altitude}, {lat}, {lon});
        """
        cur = self.conn.cursor()
        try:
            cur.execute(q)
            cur.close()
        except sqlite3.Error as err:
            print(err)

    def get_by_date(self, date):
        q = f"""
        SELECT 
        orbits.altitude, data.altitude
        FROM orbits
        INNER JOIN
        data ON orbits.date = data.date and data.date = '{date}'
        """
        cur = self.conn.cursor()
        try:
            cur.execute(q)

            for r in cur:
                print(r)

            cur.close()
        except sqlite3.Error as err:
            print(err)

    def commit(self):
        self.conn.commit()

    def get_by_shell_and_lon(self, shell, shell_delta, lon, lon_delta):

        min_lon = lon - lon_delta
        max_lon = lon + lon_delta

        if min_lon < -180:
            q = f"""
            SELECT 
            orbits.altitude, data.altitude
            FROM orbits
            INNER JOIN
            data ON orbits.date = data.date and 
                    ABS(data.l_value - {shell}) < {shell_delta} and
                    orbits.lon > -180 and
                    orbits.lon < {lon} or
                    orbits.lon > {min_lon} + 360 and
                    orbits.lon < 180
            """
        elif max_lon > 180:
            q = f"""
            SELECT 
            orbits.altitude, data.altitude
            FROM orbits
            INNER JOIN
            data ON orbits.date = data.date and 
                    ABS(data.l_value - {shell}) < {shell_delta} and
                    orbits.lon > {lon} and
                    orbits.lon < 180 or
                    orbits.lon > 0 and
                    orbits.lon < max_lon - 360
            """
        else:
            q = f"""
            SELECT 
            orbits.altitude, data.altitude
            FROM orbits
            INNER JOIN
            data ON orbits.date = data.date and 
                    ABS(data.l_value - {shell}) < {shell_delta} and
                    orbits.lon > {min_lon} and
                    orbits.lon < {max_lon} 
            """
        cur = self.conn.cursor()
        try:
            cur.execute(q)

            for r in cur:
                print(r)

            cur.close()
        except sqlite3.Error as err:
            print(err)

    def create_database(self, orbit_directory, datafile_directory):
        data_files = glob.glob(f"{datafile_directory}/**/ne-????????.txt", recursive=True)
        orbit_files = glob.glob(f"{orbit_directory}/**/ED??????.txt", recursive=True)
        for filename in data_files:
            print(filename)
            data = load_data(filename)
            for d in data:
                date, altitude, mlt, l_value, ne = d[0].isoformat(), d[1], d[2], d[3], d[4]
                self.insert_data(date, altitude, mlt, l_value, ne)
            self.commit()
        for filename in orbit_files:
            print(filename)
            orbits = load_orbits(filename)
            for d in orbits:
                date, altitude, lat, lon = d
                if date.second == 0:
                    date = date.isoformat()
                    self.insert_orbits(date, altitude, lat, lon)
            self.commit()
