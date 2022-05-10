import os
import sys
import time

import pika


def main():
    # Establish a connection to a broker on the localhost
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare queue to make sure that the queue exists.
    channel.queue_declare(queue='task_queue', durable=True)
    print('[x] Waiting for message. To exist press CTRL + C')

    def callback(ch, method, properties, body):
        print("[x] Received %r " % body.decode())
        time.sleep(body.count(b'.'))
        print("[x] Done")
        # worker delivery own ack on same channel after work done. Need auto_ack remove on channel.basic_consume
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # 1 message per work. Waiting for ACK to sending another.
    channel.basic_qos(prefetch_count=1)
    # Callback function receive messages from our 'hello' queue
    channel.basic_consume(queue="hello", on_message_callback=callback)

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
