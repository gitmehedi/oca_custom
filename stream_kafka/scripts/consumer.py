from kafka import KafkaConsumer

consumer = KafkaConsumer('mytopic', group_id='group1', bootstrap_servers=['localhost:9091'])
print('This is print.....')
for message in consumer:
    print("Changes...")

    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    # print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
    #                                       message.offset, message.key,
    #                                       message.value))
