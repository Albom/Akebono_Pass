import datetime as dt


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
    with open(filename, "rt", encoding="ascii") as file:
        table = [x.strip().split() for x in file.readlines()[1:]]

    orbits = []
    for r in table:
        if r[1] == "UT":
            break
        year = int(r[1][:2])
        year += 1900 if year > 50 else 2000
        month = int(r[1][2:4])
        day = int(r[1][4:6])
        hour = int(r[1][6:8])
        minute = int(r[1][8:10])
        second = int(r[1][10:12])
        if second == 60:
            second = 0
            minute += 1
        if minute == 60:
            minute = 0
            hour += 1
        date = dt.datetime(year, month, day, hour, minute, second)
        lat = float(r[27])
        lon = float(r[28])
        altitude = float(r[29])# - 6370.0
        orbits.append([date, altitude, lat, lon])

    return orbits
