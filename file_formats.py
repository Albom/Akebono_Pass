import datetime as dt
import bz2


def load_data(filename):

    with open(filename, encoding="ascii") as file:
        lines = [s.strip().split() for s in file.readlines()[1:] if s.strip()]

    data = []
    for r in lines:
        year = int(r[1][:2])
        year += 1900 if year > 50 else 2000
        month = int(r[1][2:4])
        day = int(r[1][4:6])
        hour = int(r[2][:2])
        minute = int(r[2][2:4])
        second = int(r[2][4:6])
        date = dt.datetime(year, month, day, hour, minute, second)
        altitude = float(r[3])
        mlt = float(r[5])
        l_value = float(r[6])
        ne = float(r[7])
        data.append([date, altitude, mlt, l_value, ne])
    return data


def load_orbits(filename):

    table = []
    with bz2.open(filename, "rt") as file:
        table = [x.strip().split() for x in file.readlines()[4:]]

    orbits = []
    for r in table:
        year = int(r[0][:2])
        year += 1900 if year > 50 else 2000
        month = int(r[0][3:5])
        day = int(r[0][6:8])
        hour = int(r[1][:2])
        minute = int(r[1][3:5])
        second = int(r[1][6:8])
        date = dt.datetime(year, month, day, hour, minute, second)
        lat = float(r[2])
        lon = float(r[3])
        altitude = float(r[4]) - 6370.0
        orbits.append([date, altitude, lat, lon])

    return orbits
