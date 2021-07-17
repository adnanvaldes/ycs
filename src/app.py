from yeelight import discover_bulbs, Bulb
from datetime import datetime, timedelta
from error_logging import *
import requests
import schedule
import logging
import time
import os

try:
    upDuration = os.environ['upDuration']
    downDuration = os.environ['downDuration']
    lat = os.environ['lat']
    lng = os.environ['lng']
    morning_start = os.environ['morning']
    evening_start = os.environ['evening']
except KeyError:
    upDuration = 60
    downDuration = 60
    lat = 49.217876
    lng = -123.142097
    morning_start = 'sunrise'
    evening_start = 'civil_twilight_end'

def to_time(time_string):
    times = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S+00:00").time()
    return str(times)

def minutes_to_ms(minutes):
    return minutes * 60000

@docker_log()
def light_scheduler(lat, lng, m_start, n_start):
    sunTimes = requests.get(f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}& formatted=0')

    if sunTimes.status_code == 200:
        sunTimes = sunTimes.json()['results']
        try:
            m_start = int(m_start)
        except ValueError:
            print('Morning start time is string, using API reference time.')
            morning = to_time(sunTimes[m_start])
            pass

        try:
            n_start = int(n_start)
        except ValueError:
            print('Evening start time is string, using API reference time.')
            evening = to_time(sunTimes[n_start])
            pass

        schedule.every().day.at(morning).do(start_winding, up=True, upDuration=upDuration).tag("Morning routine")
        print(f"Sunrise routine scheduled at {morning}")
        schedule.every().day.at(evening).do(start_winding, down=True, downDuration=downDuration).tag("Evening routine")
        print(f"Sunset routine scheduled at {evening}")

        return sunTimes

    else:
        raise StatusCode(sunTimes.status_code)


@docker_log()
def start_winding(upDuration:"minutes",downDuration:"minutes", up=False, down=False):
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

    schedule.every().minute.at(":30").do(light_scheduler, lat=lat, lng=lng, m_start=morning_start, n_start=evening_start).tag("Main scheduler")
    schedule.every(5).minutes.do(ping_bulbs).tag("Ping bulbs")
    while True:
        schedule.run_pending()
        all_jobs = schedule.get_jobs()
        print(all_jobs)
        print(upDuration, downDuration, lat, lng)
        time.sleep(5)

if __name__ == "__main__":
    main()