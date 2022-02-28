FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev -y

RUN mkdir /code
WORKDIR /code
RUN pip install pip -U
COPY requirements.txt /code/
COPY requirements /code/requirements
RUN pip install -r requirements.txt
COPY . /code/