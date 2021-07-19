# YCS (Yeelight Control Script)

A simple, configurable service to control Yeelight bulbs in a network. Lights can be turned on/off programatically, on a custom schedule, or simply set to follow sunrise and sunset (among other options).

## Table of Contents

* [General Info](#general-information)
* [Setup & Usage](#setup-&-usage)
* [Road Map](#road-map)

## General Information

YCS is a Python 3 script designed with Docker in mind. It's purpose is to gently simulate light changes in the morning and evening - a tool particularly useful for those who live in basements with poor direct sunlight. The script can be configured to, for example, begin turning on the lights at sunrise every day, over a period of 60 minutes, and/or slowly turn off the lights as evening civil twilight begins, over a different, custom period.

There are several options available (see * [Setup & Usage](#setup-&-usage)). If an option is not included or if there's any problem, create an issue with a request and I will try my best to make it happen/fix it.

## Setup & Usage

### Docker

The easiest way to use YCS is to deploy it as a docker container. The image itself is about 140 MB. The latest image is available via:

`docker pull einhard/ycs`

Once pulled, a container can be deployed and various settings can be customized via ENV variables (see [settings](###settings) for details).

You must ensure that the Docker network is the same as the host network - or, in any case, that the container can access the bulbs via the network.

Once deployed, YCS will discover all the Yeelight bulbs you have installed and will schedule them to turn on and off based on your settings - you don't have to do anything else.

If you want to confirm that YCS is working, set the update time and the morning time a few minutes ahead and wait to see if the lights change. I suggest you also set the transition time to a minute or less, since checking whether the light is changing over the 60 minute default is, well, time consuming.

*Note: The update time and any user ENVs that specify time for scheduled events are based on the host system time. However, times derived from astronomical events - sunset, twilight, etc. - are all in UTC. See [Road Map](#road-map).*

### Bare metal

If you want to run YCS directly on your computer, make sure you have Python installed. Any 3.x version should work, although it has only been tested on Python 3.8+.

Start by installing the necessary dependencies. You can either use the `requirements.txt` file or, if you have a standard Python version, simply run:

`pip install schedule` <br>
`pip install yeelight`

Download this repo, navigate to the `./src` directory and run `app.py`. Note that you'll have to set ENV variables according to your system (Linux/NT/iOS) if you don't want to use the default settings.

*Note: The update time and any user ENVs that specify time for scheduled events are based on the host system time. However, times derived from astronomical events - sunset, twilight, etc. - are all in UTC. See [Road Map](#road-map).*

### Settings

The following ENV variables are available for YCS. More may be added as the project is developed.

|ENV label| Defaults |Description |
| --- | --- | --- |
|LAT | `49.19333386092744` | FLOAT. Latitude in decimal degrees|
|LNG | `-123.17707295914504` | FLOAT. Longitude in decimal degrees|
|ON_START_TIME | `sunrise` | STR. Time when the lights will be scheduled to start turning on. Custom times must be passed in the format "HH:MM(:SS)" where seconds are optional. API derived values can be: - `sunrise`, `sunset`, `solar_noon`, `civil_twilight_begin`, `civil_twilight_end`, `nautical_twilight_begin`, `nautical_twilight_end`, `astronomical_twilight_begin`, or `astronomical_twilight_end`.
|OFF_START_TIME | `civil_twilight_end` | STR. Time when the lights will be scheduled to start turning off. Custom times must be passed in the format "HH:MM(:SS)" where seconds are optional. API derived values can be: - `sunrise`, `sunset`, `solar_noon`, `civil_twilight_begin`, `civil_twilight_end`, `nautical_twilight_begin`, `nautical_twilight_end`, `astronomical_twilight_begin`, or `astronomical_twilight_end`.
ON_TRANSITION | `60` | INT or FLOAT. Time in minutes for the lights to turn on. They will go from their last setting up to maxium brightness in the time specified. For instance, if `ON_TRANSITION=15`, the lights will be at maximum brightness 15 minutes after the specified `ON_START_TIME`.
OFF_TRANSITION | `60` | INT or FLOAT. Time in minutes for the lights to turn offn. They will go from their last setting down in brightness until turning off in the time specified. For instance, if `OFF_TRANSITION=15`, the lights will be turn off 15 minutes after the specified `OFF_START_TIME`.
SUN_UPDATE_TIME | `10:00` | STR. The time (using system time) when updated API astronomical times will be acquired - runs one per day and updates the API-based `ON_START_TIME` and `OFF_START_TIME` values.
PING_BULB | `30` | STR. In seconds, how often the current properties of the bulbs will be checked. This may be useful if the bulbs tend to disconnect from the network. One can think of it as checking for a heartbeat.

*Note: the `sunrise`, `twilight` and other specific times are downloaded by HTTP requests to [Sunrise Sunset](https://sunrise-sunset.org/api).*

*Note: The update time and any user ENVs that specify time for scheduled events are based on the host system time. However, times derived from astronomical events - sunset, twilight, etc. - are all in UTC. See Road Map.*

## Road Map

The most basic functionality is currently stable. Lights turn on/off automatically and one is able to at least somewhat simulate sunrise, sunset, etc.

Over time, the following functionality is expected to be added:

- [ ] Include localization/timezone awareness to standarize time, instead of juggling UTC vs system time.
- [ ] Create more complex transition options - such as a transition between civil twilight and astronomical twilight.
- [ ] Create Django-based webserver for a GUI that can control settings, instead of having to redeploy container with updated ENV variables.
- [ ] Add persistence to user settings by including a database.
- [ ] Add Nanoleaf light support.
- [ ] Add Phillips Hue light support.

Thank you for reading this far. If you have any suggestions, want to report bugs, or change the functionality of the script, please create an issue or make a pull request.
