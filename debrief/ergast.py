def race_schedule(requests):
    schedule = requests.get('http://ergast.com/api/f1/2012')
    return schedule.text
