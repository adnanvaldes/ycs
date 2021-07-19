
FROM python:3.8 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.8-slim


WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./src .

RUN apt-get update && apt-get upgrade --no-install-recommends --no-install-suggests -y

ENV LAT=49.19333386092744
ENV LNG=-123.17707295914504
ENV ON_START_TIME=sunrise
ENV OFF_START_TIME=civil_twilight_end
ENV ON_TRANSITION=60
ENV OFF_TRANSITION=60
ENV SUN_UPDATE_TIME=10:00
ENV PING_BULB_FREQ=30


ENV PATH=/root/.local:$PATH
CMD [ "python", "./app.py"]