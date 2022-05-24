FROM ubuntu:20.04

RUN apt update
RUN apt install -y python3 python3-pip python3-dev build-essential gcc

RUN pip3 install --upgrade pip

RUN mkdir /app
WORKDIR /app
COPY . /app

# RUN pip3 install -r requirements.txt
RUN pip3 install pika
RUN pip3 install azure-iot-hub
RUN pip3 install azure-iot-device

CMD ["python3", "hub_sender.py"]

