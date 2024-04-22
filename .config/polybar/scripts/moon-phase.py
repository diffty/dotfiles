import math
from datetime import datetime, timedelta

import ephem


def get_moon_phase_coef(d: datetime):
    curr_day_str = d.strftime("%Y-%m-%d")
    prev_day_str = (d - timedelta(days=1)).strftime("%Y-%m-%d")

    curr_m = ephem.Moon()
    curr_m.compute(curr_day_str)

    prev_m = ephem.Moon()
    prev_m.compute(prev_day_str)

    return ((2. -  curr_m.moon_phase) if curr_m.moon_phase < prev_m.moon_phase else curr_m.moon_phase) / 2.


def wrapnum(n, nmax):
    return n % nmax if n >= 0 else (nmax - (abs(n) % nmax))


moon_phase_chars = "󰽤󰽧󰽡󰽨󰽢󰽦󰽣󰽥"

moon_phase_coef = get_moon_phase_coef(datetime.now())
print(moon_phase_chars[math.floor(wrapnum((moon_phase_coef + (1. / len(moon_phase_chars) / 2.)) * len(moon_phase_chars), len(moon_phase_chars)))])
