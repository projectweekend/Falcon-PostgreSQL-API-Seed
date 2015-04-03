FROM python:2.7.9

ADD . /src/
WORKDIR /src
RUN pip install -r requirements.txt

EXPOSE 5000
