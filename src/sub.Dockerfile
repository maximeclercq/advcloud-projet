FROM ubuntu:18.04

RUN apt update
RUN apt install -y python3 python3-pip python3-dev build-essential gcc

RUN pip3 install --upgrade pip

RUN mkdir /app
WORKDIR /app
COPY . /app

# RUN pip3 install -r requirements.txt
RUN pip3 install pika

CMD ["python3", "broker_receiver.py"]

