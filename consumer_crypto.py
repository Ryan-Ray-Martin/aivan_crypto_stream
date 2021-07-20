# This script receives messages from a Kafka topic

from kafka import KafkaConsumer
import collections

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

# Call poll twice. First call will just assign partitions for our
# consumer without actually returning anything
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print (message.value.decode('utf-8'))

# Commit offsets so we won't get the same messages again

#consumer.commit()