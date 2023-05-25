import fastf1 as ff1
from fastf1 import plotting
from fastf1.ergast import Ergast
from matplotlib import pyplot as plt
from debrief.ergast import constructor_name_by_driver
import io

plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1', misc_mpl_mods=True)
ergast = Ergast()


def fastest_driver_q_lap(year: int, gp: str, identifier: str, drivers: list[str], x: str, y: str) -> io.BytesIO:
    session = ff1.get_session(year, gp, identifier)
    session.load()

    def get_driver_fastest_lap(d: str):
        return d, session.laps.pick_driver(d).pick_fastest().get_telemetry().add_distance()

    def fullname_by_code(code: str):
        df = ergast.get_driver_info(season=year)
        return df.loc[df['driverCode'].str.casefold() == code.casefold(), 'driverId'].values.item()

    fastest = list(map(get_driver_fastest_lap, drivers))
    for (driver, driver_fast_lap) in fastest:
        x_plt = driver_fast_lap[x.capitalize()]
        y_plt = driver_fast_lap[y.capitalize()]

        driver_name = fullname_by_code(driver)
        constructor = constructor_name_by_driver(driver_name, year)
        plt.plot(x_plt, y_plt, color=ff1.plotting.team_color(constructor))

    io_bytes = io.BytesIO()
    plt.savefig(io_bytes, format='png', dpi=300)
    io_bytes.flush()
    io_bytes.seek(0)
    return io_bytes
