## Ce programme est utilisé pour simuler
## l'envoi de données grâce à rabbitMQ en local.
## Dans le edge, ce script sera remplacé, 
## soit par une application gérant l'acquisition d'image de caméra..


import pika
import sys
import time
import os

host = os.environ.get('AMQP_HOST')

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.exchange_declare(exchange="logs", exchange_type="fanout")
i = 0
while i<10:
    message = ' '.join(sys.argv[1:]) or "info: Hello Word"
    channel.basic_publish(exchange="logs", routing_key="", body=message)
    print(" [x] Sent %r" % message)
    time.sleep(5)
    i+=1
connection.close()