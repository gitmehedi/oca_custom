import time
from json import dumps
from kafka import KafkaProducer

syslog = '/var/log/postgresql/postgresql-10-main.log'
sleep_time_in_seconds = 1

KF_IP = ['localhost:9091']

producer = KafkaProducer(bootstrap_servers=KF_IP, value_serializer=lambda x: dumps(x).encode('utf-8'))

try:
    with open(syslog, 'r', errors='ignore') as f:
        while True:
            for line in f:
                if line:
                    journal = {'key': 'move', 'vals': line.strip()}
                    producer.send('cassandra', value=journal)
                    print(line.strip())
            time.sleep(sleep_time_in_seconds)
except IOError as e:
    print('Cannot open the file {}. Error: {}'.format(syslog, e))