FROM python:2.7.9

RUN apt-get update && apt-get -y install default-jre

ADD . /src/
WORKDIR /src
RUN pip install -r requirements.txt

EXPOSE 5000
