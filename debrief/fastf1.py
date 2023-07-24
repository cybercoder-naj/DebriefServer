import fastf1 as ff1
from fastf1 import plotting
from fastf1.ergast import Ergast
from matplotlib import pyplot as plt
from debrief.ergast import constructor_name_by_driver
import io

plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1', misc_mpl_mods=True)
ergast = Ergast()


def fastest_lap_of_driver(year: int, gp: str, identifier: str, drivers: list[str], x_str: str, y_str: str) -> io.BytesIO:
    session = ff1.get_session(year, gp, identifier)
    session.load()

    x_str = x_str.capitalize()
    y_str = y_str.capitalize()

    def get_driver_fastest_lap(d: str):
        return d, session.laps.pick_driver(d).pick_fastest().get_telemetry().add_distance()

    def fullname_by_code(code: str):
        df = ergast.get_driver_info(season=year)
        return df.loc[df['driverCode'].str.casefold() == code.casefold(), 'driverId'].values.item()

    fastest = list(map(get_driver_fastest_lap, drivers))
    for (driver, driver_fast_lap) in fastest:
        x_plt = driver_fast_lap[x_str]
        y_plt = driver_fast_lap[y_str]

        driver_name = fullname_by_code(driver)
        constructor = constructor_name_by_driver(driver_name, year)
        plt.plot(x_plt, y_plt, color=ff1.plotting.team_color(constructor), label=driver)

    plt.clf()
    plt.rcParams['figure.figsize'] = [18, 10]
    plt.ylabel(y_str)
    plt.xlabel(x_str)
    plt.title(f"{' vs '.join(drivers)} Fastest {identifier} lap in {gp} {year}")
    plt.grid(color='#3b3a3a')
    plt.legend(loc="upper right")

    io_bytes = io.BytesIO()
    plt.savefig(io_bytes, format='png', dpi=300)
    io_bytes.flush()
    return io_bytes


def delta_time_