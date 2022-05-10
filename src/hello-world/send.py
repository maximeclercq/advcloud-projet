import pika

# Establish a connection to a broker on the localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue for sending message otherwise RabbitMQ drop the message.
channel.queue_declare(queue='hello')

# Need exchange for sending to queue.
# routing_key : queue buffer
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print("[x] Sent 'Hello World!")

# Flush network buffer and close connection
connection.close()