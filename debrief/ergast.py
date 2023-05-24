import json


def race_schedule(requests, year):
    if not 1950 <= year <= 2023:
        return None

    schedule = requests.get(f'http://ergast.com/api/f1/{year}.json')
    return json.loads(schedule.text)
