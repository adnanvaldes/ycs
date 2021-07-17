from yeelight import discover_bulbs, Bulb
from datetime import datetime, timedelta
from error_logging import *
import requests
import schedule
import logging
import time


def to_time(time_string):
    times = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S+00:00").time()
    return str(times)

def minutes_to_ms(minutes):
    return minutes * 60000

@docker_log()
def light_scheduler(latlng: tuple=(49.217876, -123.142097)):
    sunTimes = requests.get(f'https://api.sunrise-sunset.org/json?lat={latlng[0]}&lng={latlng[1]}& formatted=0')

    if sunTimes.status_code == 200:
        sunTimes = sunTimes.json()['results']
        morning = to_time(sunTimes['sunrise'])
        evening = to_time(sunTimes['civil_twilight_end'])


        schedule.every().day.at(morning).do(start_winding, up=True).tag("Morning routine")
        print(f"Sunrise routine scheduled at {morning}")
        schedule.every().day.at(evening).do(start_winding, down=True).tag("Evening routine")
        print(f"Sunset routine scheduled at {evening}")

        return sunTimes

    else:
        raise StatusCode(sunTimes.status_code)


@docker_log()
def start_winding(up=False, upDuration:"minutes"=60, down=False, downDuration:"minutes"=0.5):
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

    schedule.every().day.at("10:00").do(light_scheduler).tag("Main scheduler")
    schedule.every(5).minutes.do(ping_bulbs).tag("Ping bulbs")
    while True:
        schedule.run_pending()
        all_jobs = schedule.get_jobs()
        print(all_jobs)
        time.sleep(5)

if __name__ == "__main__":
    main()