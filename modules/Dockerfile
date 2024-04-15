FROM selenoid/chrome

USER root

RUN apt-get update && \
    apt install -y --no-install-recommends pip && \
    apt install python3.10-venv -y && \
    pip install undetected-chromedriver

WORKDIR /code

COPY requirements.txt .

RUN python3 -m venv ./env && \
    ./env/bin/pip install -r requirements.txt

COPY .. .


# Dockerfile
#ARG CHROME_VERSION
#
#FROM selenoid/chrome:${CHROME_VERSION:-latest} as selenoid_chrome
#
#
#FROM python:3.10-alpine as patcher
#
#RUN pip install undetected-chromedriver
#
#COPY --from=selenoid_chrome /usr/bin/chromedriver /usr/bin/chromedriver
#
#COPY patch_driver.py .
#
#RUN python3 patch_driver.py
#
#
#FROM selenoid_chrome
#
#USER root
#
#COPY --from=patcher /usr/bin/chromedriver /usr/bin/chromedriver
#
#ENV DRIVER_ARGS="--headless=new --user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36' --verbose"
#
#RUN AAA=$(echo '#!/bin/bash\necho $DRIVER_ARGS' ; cat /entrypoint.sh ; ) && echo "$AAA" > /entrypoint.sh
#
#USER selenium