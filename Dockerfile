
FROM python:3.8 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.8-slim


WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./src .

RUN apt-get update && apt-get upgrade --no-install-recommends --no-install-suggests -y

ARG UP_DURATION=60
ENV upDuration=${UP_DURATION}
ARG DOWN_DURATION=60
ENV downDuration=${DOWN_DURATION}
ARG LAT=49.217876
ENV lat=${LAT}
ARG LNG=-123.142097
ENV lng=${LNG}
ARG MORNING=sunrise
ENV morning=${MORNING}
ARG EVENING=civil_twilight_end
ENV evening=${EVENING}
ENV PATH=/root/.local:$PATH
CMD [ "python", "./app.py" ]