import pika
import socket
import struct
import os.path

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="logs", exchange_type="fanout")

result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange="logs", queue=queue_name)

print(" [*] Waiting for logs. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print("[x] %r" % body)
    send_to_other_process(body)


def send_to_other_process(body):
    print("Connecting...")
    if os.path.exists("/tmp/python_unix_sockets_example"):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        client.connect("/tmp/python_unix_sockets_example")
        print("Ready.")
        print("Ctrl-C to quit.")
        print("SEND:", body)
        client.send(body)
        client.close()
    else:
        print("Couldn't Connect!")
        print("Done")


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
