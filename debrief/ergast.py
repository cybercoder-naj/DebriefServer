import json


def race_schedule(requests, year):
    schedule = requests.get(f'http://ergast.com/api/f1/{year}.json')
    return json.loads(schedule.text)
