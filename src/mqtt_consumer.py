import argparse
import os
import json
import logging
import socket
import paho.mqtt.client as mqtt


class MqttConsumer():

    def __init__(self, mqtt_host, mqtt_port, mqtt_topic):
        self.mqtt_host  = mqtt_host
        self.mqtt_port  = mqtt_port
        self.mqtt_topic = mqtt_topic
        self.mqtt = mqtt.Client()
        self.mqtt.enable_logger()
        self.mqtt.on_connect = self.mqtt_on_connect
        self.mqtt.on_message = self.mqtt_on_message
        logging.debug(f'Params: {self.__dict__}')

    def run(self):
        print(f"host: {self.mqtt_host}, port: {self.mqtt_port}, topic: {self.mqtt_topic}")
        self.mqtt.connect(self.mqtt_host, self.mqtt_port)
        self.mqtt.subscribe(self.mqtt_topic)
        self.mqtt.loop_forever()

    @staticmethod
    def mqtt_on_connect(client, userdata, flags, rc):
        logging.info(f'Connected with result code {rc}')

    def mqtt_on_message(self, client, userdata, msg):
        logging.debug(f'Message on topic {msg.topic}. {len(msg.payload)} bytes')
        try:
            message = msg.payload.decode()
            logging.debug(f'Topic {msg.topic}: {message}')
            print("[x] %r" % msg)
            # send_to_socket(message)
        except Exception as e:
            logging.exception('Failed to process MQTT message: ' + str(e))

    def send_to_socket(self, message):
        print("Connecting...")
        if os.path.exists("/tmp/python_unix_sockets_example"):
            client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            client.connect("/tmp/python_unix_sockets_example")
            print("Ready.")
            print("Ctrl-C to quit.")
            print("SEND:", message)
            client.send(message)
            client.close()
        else:
            print("Couldn't Connect!")
            print("Done")

def get_argument_parser():
    parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--help',            action='help',       help='Show this help message and exit')
    parser.add_argument('-v', '--verbose',   action='store_true', help='Verbose logging')
    parser.add_argument('-h', '--host',      default=os.environ.get('MQTT_HOST',  '127.0.0.1'),    help='MQTT broker host')
    parser.add_argument('-p', '--port',      default=os.environ.get('MQTT_PORT',  1883), type=int, help='MQTT broker port')
    parser.add_argument('-t', '--topic',     default=os.environ.get('MQTT_TOPIC', '#'),            help='MQTT topic')
    return parser

def main():
    args = get_argument_parser().parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    mqtt_consumer = MqttConsumer(mqtt_host=args.host, 
                                 mqtt_port=args.port, 
                                 mqtt_topic=args.topic)

    mqtt_consumer.run()


if __name__ == '__main__':
    main()