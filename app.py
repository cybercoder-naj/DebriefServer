import base64

import requests
from flask import Flask, request, send_file
from debrief.ergast import race_schedule
import debrief.fastf1

app = Flask(__name__)

statuses = {
    'ok': 200,
    'created': 201,
    'badrequest': 400,
    'unauthorized': 401,
    'forbidden': 403,
    'notfound': 404,
}


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/race-schedule/<year>')
def get_race_schedule(year):
    response = race_schedule(int(year))
    if response is None:
        return f'Cannot fetch schedule for {year}.', statuses['notfound']

    return response


@app.route('/fastest-laps/line-graph')
def get_line_graph():
    x = request.args.get('x')
    y = request.args.get('y')
    year = int(request.args['year'])
    gp = request.args['gp']
    session = request.args['session']
    drivers = request.args['drivers'].split(',')

    response = debrief.fastf1.fastest_driver_q_lap(year, gp, session, drivers, x, y)
    return base64.b64encode(response.read()).decode()


if __name__ == '__main__':
    app.run()
