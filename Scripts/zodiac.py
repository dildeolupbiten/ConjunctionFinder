# -*- coding: utf-8 -*-

from .constants import PLANETS
from .modules import dt, os, swe
from .utilities import convert_degree, reverse_convert_degree


swe.set_ephe_path(os.path.join(os.getcwd(), "Eph"))


class Zodiac:
    def __init__(self, year, month, day):
        self.jd = self.julday(year, month, day)["JD"]
        
    @staticmethod
    def select_calendar(year, month, day):
        if year > 1582:
            if year > 9999:
                return swe.GREG_CAL
            time1 = dt.strptime(f"{day}.{month}.{year}", "%d.%m.%Y")
            time2 = dt.strptime("15.10.1582", "%d.%m.%Y")
            if (time2 - time1).days >= 0:
                return swe.JUL_CAL
            else:
                return swe.GREG_CAL
        else:
            return swe.JUL_CAL
        
    def julday(self, year, month, day):
        jd = swe.julday(
            year,
            month,
            day,
            0,
            self.select_calendar(year, month, day)
        )
        deltat = swe.deltat(jd)
        return {
            "JD": round(jd + deltat, 6),
            "TT": round(deltat * 86400, 1)
        }

    def planet_pos(self, planet):
        degree = swe.calc(self.jd, planet)[0]
        if isinstance(degree, tuple):
            degree = degree[0]
        calc = convert_degree(degree=degree)
        return calc[1], reverse_convert_degree(calc[0], calc[1])

    def patterns(self, planets):
        return [
            (key,) + self.planet_pos(planet=value)
            for key, value in PLANETS.items()
            if key in planets
        ]
