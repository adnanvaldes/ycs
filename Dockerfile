
FROM python:3.8 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.8-slim


WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./src .

RUN apt-get update && apt-get upgrade --no-install-recommends --no-install-suggests -y

ARG ON_TRANSITION=60
ENV ON_TRANSITION=${ON_TRANSITION}
ARG OFF_TRANSITION=60
ENV OFF_TRANSITION=${OFF_TRANSITION}
ARG LAT=49.217876
ENV LAT=${LAT}
ARG LNG=-123.142097
ENV LNG=${LNG}
ARG ON_START_TIME=sunrise
ENV ON_START_TIME=${ON_START_TIME}
ARG OFF_START_TIME=civil_twilight_end
ENV OFF_START_TIME=${OFF_START_TIME}
ARG SUN_UPDATE_TIME=10:00
ENV SUN_UPDATE_TIME=${SUN_UPDATE_TIME}
ARG PING_BULB_FREQ=30
ENV PING_BULB_FREQ=${PING_BULB_FREQ}


ENV PATH=/root/.local:$PATH
CMD [ "python", "./app.py"]