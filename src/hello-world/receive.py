import os
import sys

import pika


def main():
    # Establish a connection to a broker on the localhost
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare queue to make sure that the queue exists.
    channel.queue_declare(queue='hello')

    # callback call when receive message.
    def callback(ch, method, properties, body):
        print("[x] Received %r" % body)

    # Callback function receive messages from our 'hello' queue
    channel.basic_consume(queue="hello", auto_ack=True, on_message_callback=callback)

    print('[x] Waiting for message. To exist press CTRL + C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
