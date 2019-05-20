import pika
import time
import json
import random

from config import RABBIT_HOST, RABBIT_PORT

def try_connect(conn_params):
    try:
        return pika.BlockingConnection(conn_params)
    except pika.exceptions.AMQPConnectionError:
        print('rabbitmq not ready, retrying')
        time.sleep(5)
        return try_connect(conn_params)


conn_params = pika.ConnectionParameters(RABBIT_HOST, RABBIT_PORT)
conn = try_connect(conn_params)
chan = conn.channel()

chan.queue_declare(queue='mailer')


def send_mail(to, subject, text):
    msg = json.dumps({
        'to': to,
        'subject': subject,
        'text': text
    })
    chan.basic_publish(
        exchange='',
        routing_key='mailer',
        body=msg
    )
    print('mailed: ', to, subject, text, end='\n\n')
