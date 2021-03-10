# FROM python:3.7-alpine3.8
# # Bootstrap the image so that it includes all of our dependencies

# #fix alpine images install psycopg2 error
# RUN apk update && apk add  postgresql-dev gcc  musl-dev

# # Setup locale
# RUN export LC_ALL=en_US.UTF-8
# RUN export LANG=en_US.UTF-8
# RUN export LANGUAGE=en_US.UTF-8
 
# # copy the contents of the cloud-native-app(i.e. complete application) folder into the container at build time
# RUN mkdir -p app
# WORKDIR app
# ADD . .

 
# # Create Virtual environment
# RUN pip install  virtualenv 
# RUN mkdir -p /venv/
# RUN virtualenv venv 

# RUN chmod 777 venv/bin/activate
# RUN venv/bin/activate
# # Python dependencies inside the virtualenv
# # RUN venv/bin/pip3 install --upgrade setuptools
# RUN pip install -r requirements.txt
# RUN export DEBUG=False
# # expose a port for the flask development server
# EXPOSE 8080
 
# # Running our flask application 
# CMD  python app.py


# FROM ubuntu:16.04
FROM jianlv/pip-cache-ubuntu:v1.1
# FROM rcarmo/ubuntu-python:3.7-amd64
MAINTAINER jianlv <duke.lv@hotmail.com>
 
# no tty
# ENV DEBIAN_FRONTEND noninteractive
 
# get up to date
# RUN apt-get -qq update --fix-missing
 
# Bootstrap the image so that it includes all of our dependencies
# RUN apt-get -qq install python3  python-dev python-virtualenv python3-pip --assume-yes
# RUN apt-get install build-essential autoconf libtool libssl-dev libffi-dev --assume-yes

RUN export LC_ALL=en_US.UTF-8
RUN export LANG=en_US.UTF-8
RUN export LANGUAGE=en_US.UTF-8

COPY ../../* /usr/app
WORKDIR /usr/app
RUN export FLASK_APP=app.py

RUN /venv/bin/pip3 install --upgrade pip -i http://192.168.12.199:8081/repository/ifaios-pypi-group/simple --trusted-host 192.168.12.199
# RUN /venv/bin/pip3 install -r requirements/common.txt -i https://pypi.doubanio.com/simple/
RUN /venv/bin/pip3 install -r requirements/common.txt
 
EXPOSE 8080

RUN chmod +777 ./boot.sh
ENTRYPOINT ["./boot.sh"]