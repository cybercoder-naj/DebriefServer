import base64
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
import io

plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1', misc_mpl_mods=True)


def fastest_driver_q_lap():
    year = 2019
    gp = 'Monza'
    identifier = 'Q'
    driver = 'LEC'
    constructor = 'Ferrari'

    session = ff1.get_session(year, gp, identifier)
    session.load()

    fastest = session.laps.pick_driver(driver).pick_fastest().get_telemetry()
    s = fastest['Speed']
    t = fastest['Time']

    plt.plot(t, s, color=ff1.plotting.team_color(constructor))

    io_bytes = io.BytesIO()
    plt.savefig(io_bytes, format='png')
    io_bytes.seek(0)
    fig_base64 = base64.b64encode(io_bytes.read()).decode()
    return fig_base64
