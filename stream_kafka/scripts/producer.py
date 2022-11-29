from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['localhost:9091'])

# Asynchronous by default


for msg in range(10):
    data = "Message {0}".format(msg)
    # producer.send('my-topic', data)
    msg = b'raw_bytes'
    print(msg)
    producer.send('mytopic', msg)

# Block for 'synchronous' sends
# try:
#     record_metadata = future.get(timeout=10)
# except KafkaError:
#     # Decide what to do if produce request failed...
#     pass
# # Successful result returns assigned partition and offset
# print (record_metadata.topic)
# print (record_metadata.partition)
# print (record_metadata.offset)

# produce keyed messages to enable hashed partitioning
# producer.send('my-topic', key=b'foo', value=b'bar')
