import datetime as dt
from dataclasses import dataclass
from database import Database


@dataclass
class Parameters:
    start_date: dt.date
    end_date: dt.date
    shell: float
    shell_delta: float
    longitude: float
    longitude_delta: float
    output_filename: str


class Search:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters

    def run(self):

        db = Database()
        db.connect("akebono.db")
        results = db.get_by_date_shell_lon(
            self.parameters.start_date,
            self.parameters.end_date,
            self.parameters.shell,
            self.parameters.shell_delta,
            self.parameters.longitude,
            self.parameters.longitude_delta,
        )
        db.close()

        with open(self.parameters.output_filename, "wt", encoding="ascii") as file:
            file.write(f"{'# date':20s} {'DOY':>10s} {'Alt':>8s} {'Lat':>6s} {'Lon':>6s} {'Alt':>8s} {'MLT':>6s} {'L':>6s} {'Ne':>10s}\n")
            for r in results:
                date = dt.datetime.fromisoformat(r[0])
                doy = float(date.strftime("%j")) + (date.hour + date.minute / 60 + date.second / 3600) / 24
                file.write(f"{r[0]:20s} {doy:10.6f} {r[1]:8.2f} {r[2]:6.2f} {r[3]:6.2f} {r[4]:8.2f} {r[5]:6.3f} {r[6]:6.3f} {r[7]:10.3f}\n")
