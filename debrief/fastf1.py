import fastf1 as ff1
from fastf1 import plotting
from fastf1.ergast import Ergast
import matplotlib
from matplotlib import pyplot as plt
from debrief.ergast import constructor_name_by_driver
import io
import sys

matplotlib.use('Agg')
plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1', misc_mpl_mods=True)
ergast = Ergast()

def fullname_by_code(code: str, year: int):
    df = ergast.get_driver_info(season=year)
    return df.loc[df['driverCode'].str.casefold() == code.casefold(), 'driverId'].values.item()

"""
    year must be a valid year. Presumely after year 2000
    gp must be the name of the circuit. a number can be provided as well to indicate the round number of the year.
    identifier must be like FP1 FP2 Q S SS, R etc
    drivers need to be comma separated, 3-letter driver code
    x_str, y_str should what you wish to plot.

    this is will always look for the fastest lap in the session and not any lap specified.
"""
def fastest_lap_of_driver(year: int, gp: "str | int", identifier: str, drivers: list[str], x_str: str, y_str: str) -> io.BytesIO:
    session = ff1.get_session(year, gp, identifier)
    session.load()

    x_str = x_str.capitalize()
    y_str = y_str.capitalize()

    def get_driver_fastest_lap(d: str):
        return d, session.laps.pick_driver(d).pick_fastest().get_telemetry().add_distance()


    fastest = list(map(get_driver_fastest_lap, drivers))
    plt.clf()
    for (driver, driver_fast_lap) in fastest:
        x_plt = driver_fast_lap[x_str]
        y_plt = driver_fast_lap[y_str]

        driver_name = fullname_by_code(driver, year)
        constructor = constructor_name_by_driver(driver_name, year)
        plt.plot(x_plt, y_plt, color=ff1.plotting.team_color(constructor), label=driver)

    plt.rcParams['figure.figsize'] = [18, 10]
    plt.ylabel(y_str)
    plt.xlabel(x_str)
    plt.title(f"{' vs '.join(drivers)} Fastest {identifier} lap in {gp} {year}")
    plt.grid(color='#3b3a3a')
    plt.legend(loc="upper right")

    io_bytes = io.BytesIO()
    plt.savefig(io_bytes, format='png', dpi=300)
    io_bytes.seek(0)
    return io_bytes


def delta_time_between_drivers(year: int, gp: str, identifier: str, drivers: list[str], lap: int) -> "io.BytesIO | None":
    session = ff1.get_session(year, gp, 'Q') # TODO change the 'Q' to identifier
    session.load()

    if len(drivers) != 2:
        return None

    # driver1 = session.laps.pick_lap(lap).pick_driver(drivers[0]).get_telemetry().add_distance()[['Time', 'Speed', 'Distance']]
    # driver2 = session.laps.pick_lap(lap).pick_driver(drivers[1]).get_telemetry().add_distance()[['Time', 'Speed', 'Distance']]
    
    # TODO remove below
    driver1 = session.laps.pick_driver(drivers[0]).pick_fastest().get_telemetry().add_distance()[['Time', 'Distance']]
    driver2 = session.laps.pick_driver(drivers[1]).pick_fastest().get_telemetry().add_distance()[['Time', 'Distance']]

    max_dist = max(driver1.iloc[-1, 1], driver2.iloc[-1, 1])
    mini_sector_dist = max_dist / 100 # TODO make this a parm

    curr_dist = 0
    delta = []
    x_dist = []
    d1_dist = 0
    d1_idx = 0
    d2_dist = 0
    d2_idx = 0
    while curr_dist < max_dist:
        while d1_dist < curr_dist:
            d1_dist = driver1.iloc[d1_idx, 1]
            if d1_idx + 1 < len(driver1):
                d1_idx += 1
            else:
                break
        d1_time = driver1.iloc[d1_idx, 0]

        while d2_dist < curr_dist:
            d2_dist = driver2.iloc[d2_idx, 1]
            if d2_idx + 1 < len(driver2):
                d2_idx += 1
            else:
                break
        d2_time = driver2.iloc[d2_idx, 0]

        delta.append((d2_time - d1_time).total_seconds())

        x_dist.append(curr_dist)
        curr_dist += mini_sector_dist

    x_dist = list(map(lambda d: (d / x_dist[-1]) * 100, x_dist))

    plt.clf()

    constructor1 = constructor_name_by_driver(fullname_by_code(drivers[0], year), year)
    constructor2 = constructor_name_by_driver(fullname_by_code(drivers[1], year), year)
    # plt.plot(x_dist, list(map(lambda d: 0 if d <= 0 else d, delta)), color=ff1.plotting.team_color(constructor1), label=drivers[0])
    # plt.plot(x_dist, list(map(lambda d: 0 if d > 0 else d, delta)), color=ff1.plotting.team_color(constructor2), label=drivers[1])
    # plt.axhline(y=0, color='white', linestyle='-')
    plt.plot(x_dist, delta)

    plt.ylabel("Delta")
    plt.xlabel("Distance (%)")
    plt.title(f"Insert a title")
    plt.grid(color='#3b3a3a')
    plt.legend(loc="upper right")

    io_bytes = io.BytesIO()
    plt.savefig(io_bytes, format='png', dpi=300)
    io_bytes.seek(0)
    return io_bytes