import requests
from flask import Flask
from debrief.ergast import race_schedule

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/race-schedule/<year>')
def get_race_schedule(year):
    return race_schedule(requests, year)


if __name__ == '__main__':
    app.run()
