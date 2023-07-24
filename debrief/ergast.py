import json
import requests


def race_schedule(year: int):
    if not 1950 <= year <= 2023:
        return None

    schedule = requests.get(f'http://ergast.com/api/f1/{year}.json')
    return json.loads(schedule.text)


def constructor_name_by_driver(driver: str, year: int) -> "str | None":
    if not 1950 <= year <= 2023:
        return None

    driver_info = requests.get(f'http://ergast.com/api/f1/{year}/drivers/{driver}/constructors.json')
    driver_info = json.loads(driver_info.text)
    return driver_info['MRData']['ConstructorTable']['Constructors'][0]['name']
