from yeelight import discover_bulbs, Bulb
from datetime import datetime, timedelta
from error_logging import *
import requests
import schedule
import logging
import time
import sys
import os

try:
    upDuration = int(os.environ['ON_TRANSITION_PERIOD'])
    downDuration = int(os.environ['OFF_TRANSITION_PERIOD'])
    lat = os.environ['LAT']
    lng = os.environ['LNG']
    morning_start = os.environ['ON_START_TIME']
    evening_start = os.environ['OFF_START_TIME']
    update_time = os.environ['SUN_UPDATE_TIME']
    ping_bulb_freq = int(os.environ['PING_BULB_FREQ'])
    envs = True

except KeyError:
    sys.stderr.write("ERROR - COULD NOT PARSE AT LEAST ONE ENV VARIABLE. USING DEFAULT VALUES.")
    upDuration = 60
    downDuration = 60
    lat = 49.217876
    lng = -123.142097
    update_time = "10:00"
    morning_start = 'sunrise'
    evening_start = 'civil_twilight_end'
    ping_bulb_freq = 30

def to_time(time_string):
    times = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S+00:00").time()
    return str(times)

def minutes_to_ms(minutes):
    return minutes * 60000

@docker_log()
def light_scheduler(lat, lng, morning, evening, upDuration=upDuration, downDuration=downDuration):
    sunTimes = requests.get(f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0')

    if sunTimes.status_code == 200:
        sunTimes = sunTimes.json()['results']

        if envs:
            morning = to_time(sunTimes[morning_start])
            evening = to_time(sunTimes[evening_start])

        schedule.every().day.at(morning).do(start_winding, up=True, upDuration=upDuration).tag("Morning routine")
        print(f"Sunrise routine scheduled at {morning}")
        schedule.every().day.at(evening).do(start_winding, down=True, downDuration=downDuration).tag("Evening routine")
        print(f"Sunset routine scheduled at {evening}")

        return sunTimes

    else:
        raise StatusCode(sunTimes.status_code)


@docker_log()
def start_winding(upDuration=upDuration, downDuration=downDuration, up=False, down=False):
    for bulb in discover_bulbs():
        if up:
            print(f"Beginning wind-up routine - complete at {datetime.utcnow() + timedelta(minutes=upDuration)}")
            Bulb(bulb['ip'], effect='smooth', duration=minutes_to_ms(upDuration), auto_on=True).turn_on()
            return schedule.CancelJob

        elif down:
            print(f"Beginning wind-down routine - complete at {datetime.utcnow() + timedelta(minutes=downDuration)}")
            Bulb(bulb['ip'], effect='smooth', duration=minutes_to_ms(downDuration)).turn_off()
            return schedule.CancelJob
    return schedule.CancelJob

@docker_log()
def ping_bulbs():
    return discover_bulbs()

def main():
    logging.basicConfig()
    schedule_logger = logging.getLogger('schedule')
    schedule_logger.setLevel(level=logging.DEBUG)

    schedule.every().day.at(update_time).do(light_scheduler, lat=lat, lng=lng, morning=morning_start, evening=evening_start).tag("Main scheduler")
    schedule.every(ping_bulb_freq).seconds.do(ping_bulbs).tag("Ping bulbs")
    while True:
        schedule.run_pending()
        all_jobs = schedule.get_jobs()
        print(all_jobs)
        time.sleep(1)