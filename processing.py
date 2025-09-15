import datetime as dt
from dataclasses import dataclass


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
        date = self.parameters.start_date
        while date <= self.parameters.end_date:

            date += dt.timedelta(days=1)
