FROM python:2.7.9

RUN apt-get update && apt-get -y install default-jre unzip
RUN wget http://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/3.2.1/flyway-commandline-3.2.1.zip && unzip flyway-commandline-3.2.1.zip -d /opt && chmod a+x /opt/flyway-3.2.1/flyway
ENV PATH $PATH:/opt/flyway-3.2.1

ADD . /src/
WORKDIR /src
RUN pip install -r requirements.txt

EXPOSE 5000
