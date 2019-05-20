import pika
import time
import json
import random
import yagmail
import traceback
import sys

from config import \
    RABBIT_HOST, RABBIT_PORT, \
    SMTP_USER, SMTP_PASSWORD, \
    SMTP_HOST, SMTP_PORT

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

yag = yagmail.SMTP(
    SMTP_USER, SMTP_PASSWORD,
    SMTP_HOST, SMTP_PORT
)


def send_mail(destination_mail, subject, text):
    yag.send(to=destination_mail, subject=subject, contents=[text])


def callback(ch, method, properties, body):
    print(body)
    j = json.loads(body)
    send_mail(j['to'], j['subject'], j['text'])
    chan.basic_ack(method.delivery_tag)

chan.queue_declare('mailer')
chan.basic_consume('mailer', callback)

try:
    chan.start_consuming()
except KeyboardInterrupt:
    chan.stop_consuming()
except Exception:
    chan.stop_consuming()
    traceback.print_exc(file=sys.stdout)
