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

except KeyError:
    sys.stderr.write("ERROR - COULD NOT PARSE AT LEAST ONE ENV VARIABLE. USING DEFAULT VALUES.")
    upDuration = 60
    downDuration = 60
    lat = 49.217876
    lng = -123.142097
    morning_start = 'sunrise'
    evening_start = 'civil_twilight_end'
    update_time = "10:00"
    ping_bulb_freq = 15

def to_time(time_string):
    times = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S+00:00").time()
    return str(times)

def minutes_to_ms(minutes):
    return minutes * 60000

@docker_log()
def light_scheduler(lat, lng, m_start, n_start):
    sunTimes = requests.get(f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0')

    if sunTimes.status_code == 200:
        sunTimes = sunTimes.json()['results']
        try:
            m_start = int(m_start)
        except ValueError:
            sys.stdout.write('Morning start time is string, using API reference time.')
            morning = to_time(sunTimes[m_start])
            pass

        try:
            n_start = int(n_start)
        except ValueError:
            sys.stdout.write('Evening start time is string, using API reference time.')
            evening = to_time(sunTimes[n_start])
            pass

        schedule.every().day.at(morning).do(start_winding, up=True, upDuration=upDuration).tag("Morning routine")
        sys.stdout.write(f"Sunrise routine scheduled at {morning}")
        schedule.every().day.at(evening).do(start_winding, down=True, downDuration=downDuration).tag("Evening routine")
        sys.stdout.write(f"Sunset routine scheduled at {evening}")

        return sunTimes

    else:
        raise StatusCode(sunTimes.status_code)


@docker_log()
def start_winding(upDuration:"minutes",downDuration:"minutes", up=False, down=False):
    for bulb in discover_bulbs():
        if up:
            sys.stdout.write(f"Beginning wind-up routine - complete at {datetime.utcnow() + timedelta(minutes=upDuration)}")
            Bulb(bulb['ip'], effect='smooth', duration=minutes_to_ms(upDuration), auto_on=True).turn_on()
            return schedule.CancelJob

        elif down:
            sys.stdout.write(f"Beginning wind-down routine - complete at {datetime.utcnow() + timedelta(minutes=downDuration)}")
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

    schedule.every().day.at(update_time).do(light_scheduler, lat=lat, lng=lng, m_start=morning_start, n_start=evening_start).tag("Main scheduler")
    schedule.every(ping_bulb_freq).seconds.do(ping_bulbs).tag("Ping bulbs")
    while True:
        schedule.run_pending()
        schedule.get_jobs()
        time.sleep(5)

if __name__ == "__main__":
    main()