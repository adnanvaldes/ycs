
FROM python:3.8 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.8-slim


WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./src .

RUN apt-get update && apt-get upgrade --no-install-recommends --no-install-suggests -y

ARG ON_TRANSITION_PERIOD=60
ENV ON_TRANSITION_PERIOD=${ON_TRANSITION_PERIOD}
ARG OFF_TRANSITION_PERIOD=60
ENV OFF_TRANSITION_PERIOD=${OFF_TRANSITION_PERIOD}
ARG LAT=49.217876
ENV LAT=${LAT}
ARG LNG=-123.142097
ENV LNG=${LNG}
ARG ON_START_TIME=sunrise
ENV ON_START_TIME=${ON_START_TIME}
ARG OFF_START_TIME=civil_twilight_end
ENV OFF_START_TIME=${OFF_START_TIME}
ENV PATH=/root/.local:$PATH
ARG SUN_UPDATE_TIME=10:00
ENV SUN_UPDATE_TIME=${SUN_UPDATE_TIME}
ARG PING_BULB_FREQ=5
ENV PING_BULB_FREQ=${PING_BULB_FREQ}
CMD [ "python", "./app.py" ]