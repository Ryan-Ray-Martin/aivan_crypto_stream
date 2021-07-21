# This script receives messages from a Kafka topic

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "crypto-topic",
    auto_offset_reset="latest",
    bootstrap_servers="kafka-37aaaea2-ryanraymartin-d8fc.aivencloud.com:22539",
    client_id="demo-client-1",
    group_id="demo-group",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
)

# a simple consumer method to view topic output
for message in consumer:
    print(message.value.decode('utf-8'))

#consumer.commit()