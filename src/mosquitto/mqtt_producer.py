import argparse
import logging
import os
import time
import paho.mqtt.client as mqtt

class MqttProducer():

    def __init__(self, mqtt_host, mqtt_port, mqtt_topic, message):
        self.mqtt_host  = mqtt_host
        self.mqtt_port  = mqtt_port
        self.mqtt_topic = mqtt_topic
        self.message = message
        self.mqtt = mqtt.Client()
        self.mqtt.enable_logger()
        self.mqtt.on_connect = self.mqtt_on_connect
        logging.debug(f'Params: {self.__dict__}')

    def run(self):
        print(f"host: {self.mqtt_host}, port: {self.mqtt_port}, topic: {self.mqtt_topic}")
        # self.mqtt.loop_forever()
        try:
            while True:
                self.mqtt.connect(self.mqtt_host, self.mqtt_port)
                self.mqtt.loop_start()
                self.mqtt.publish(self.mqtt_topic, self.message)
                print(" [x] Sent %r" % self.message)
                self.mqtt.loop_stop()
                time.sleep(5)
        except KeyboardInterrupt:
            print("interrupted")
            self.mqtt.disconnect()


    @staticmethod
    def mqtt_on_connect(client, userdata, flags, rc):
        logging.info(f'Connected with result code {rc}')
        print("connected OK")

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

    mqtt_consumer = MqttProducer(mqtt_host=args.host, 
                                 mqtt_port=args.port, 
                                 mqtt_topic=args.topic,
                                 message="Hello World!")

    mqtt_consumer.run()


if __name__ == '__main__':
    main()