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
    on_transition = int(os.environ['ON_TRANSITION'])
    off_transition = int(os.environ['OFF_TRANSITION'])
    lat = os.environ['LAT']
    lng = os.environ['LNG']
    morning = os.environ['ON_START_TIME']
    evening = os.environ['OFF_START_TIME']
    update_time = os.environ['SUN_UPDATE_TIME']
    ping_bulb_freq = int(os.environ['PING_BULB_FREQ'])
    envs = True

except KeyError:
    sys.stderr.write("ERROR - COULD NOT PARSE AT LEAST ONE ENV VARIABLE. USING DEFAULT VALUES.")
    on_transition = 60
    off_transition = 60
    lat = 49.217876
    lng = -123.142097
    update_time = "10:00"
    morning = 'sunrise'
    evening = 'civil_twilight_end'
    ping_bulb_freq = 30

def to_time(time_string):
    times = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S+00:00").time()
    return str(times)

def minutes_to_ms(minutes):
    return minutes * 60000

@docker_log()
def light_scheduler(lat, lng, morning, evening, on_transition=on_transition, off_transition=off_transition):
    sunTimes = requests.get(f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0')

    if sunTimes.status_code == 200:
        sunTimes = sunTimes.json()['results']

        if envs:
            morning = to_time(sunTimes[morning])
            evening = to_time(sunTimes[evening])

        schedule.every().day.at(morning).do(start_winding, up=True, on_transition=on_transition).tag("Morning routine")
        logging.debug(f"Sunrise routine scheduled at {morning}")
        schedule.every().day.at(evening).do(start_winding, down=True, off_transition=off_transition).tag("Evening routine")
        logging.debug(f"Sunset routine scheduled at {evening}")

        return sunTimes

    else:
        raise StatusCode(sunTimes.status_code)


@docker_log()
def start_winding(on_transition=on_transition, off_transition=off_transition, up=False, down=False):
    for bulb in discover_bulbs():
        if up:
            logging.debug(f"Beginning wind-up routine - complete at {datetime.utcnow() + timedelta(minutes=on_transition)}")
            Bulb(bulb['ip'], effect='smooth', duration=minutes_to_ms(on_transition), auto_on=True).turn_on()

        elif down:
            logging.debug(f"Beginning wind-down routine - complete at {datetime.utcnow() + timedelta(minutes=off_transition)}")
            Bulb(bulb['ip'], effect='smooth', duration=minutes_to_ms(off_transition)).turn_off()
    return schedule.CancelJob

@docker_log()
def ping_bulbs():
    return discover_bulbs()

def main():

    logger.warning("YOU ARE ON A DEV BRANCH. THINGS MAY BE BROKEN!")

    schedule.every().day.at(update_time).do(light_scheduler, lat=lat, lng=lng, morning=morning, evening=evening).tag("Main scheduler")
    schedule.every(ping_bulb_freq).seconds.do(ping_bulbs).tag("Ping bulbs")
    while True:
        schedule.run_pending()
        all_jobs = schedule.get_jobs()
        logger.info(all_jobs)
        logger.warning("YOU ARE ON A DEV BRANCH. THINGS MAY BE BROKEN!")
        test(2)
        time.sleep(5)

if __name__ == "__main__":
    main()
