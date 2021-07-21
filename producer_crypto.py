# Be sure to pip install polygon-api-client

import time
import json
import config
import logging
import collections
from kafka import KafkaProducer
from websocket_client import WebSocketClient, CRYPTO_CLUSTER
from datetime import datetime as dt


producer = KafkaProducer(
    bootstrap_servers="kafka-37aaaea2-ryanraymartin-d8fc.aivencloud.com:22539",
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
    acks=0,
    batch_size=0
)

""" This method below processes quotes to calculate the spread from
the polygon.io websocket, and then sends the instances to the crypto-topic
 producer."""

def my_custom_process_message(message):

    TICK_INSTANCE = json.loads(message)[0]['ev'] == 'XQ'
    crypto_data = {}
    try:
        if TICK_INSTANCE:
            message_str = (json.loads(message)[0])
            crypto_data['timestamp'] = dt.fromtimestamp(
                message_str['t']/1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            crypto_data['symbol'] = message_str['pair']
            crypto_data['spread'] = message_str['ap']-message_str['bp']
            #print(message_str)
            producer.send('crypto-topic',value=crypto_data)
        else:
            pass
    except Exception as e:
        logging.error("{}".format(e.args))
    
def my_custom_error_handler(ws, error):
    print("this is my custom error handler", error)


def my_custom_close_handler(ws):
    print("this is my custom close handler")


def main():
    key = config.POLYGON_API
    my_client = WebSocketClient(CRYPTO_CLUSTER, key, my_custom_process_message)
    my_client.run_async()

    my_client.subscribe("XQ.BTC-USD")
    time.sleep(1)

    #my_client.close_connection()


if __name__ == "__main__":
    main()