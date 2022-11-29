from kafka import KafkaConsumer
from cassandra.cluster import Cluster
import random, string, time
from json import loads

# PORT = 9042
# IP = ['127.0.0.1']
# KEYSPACE = 'test_keyspace'

# cluster = Cluster(IP, port=PORT)
# cursor = cluster.connect(keyspace=KEYSPACE)

consumer = KafkaConsumer('cassandra',
                         bootstrap_servers=['localhost:9091'],
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='my-group',
                         value_deserializer=lambda x: loads(x.decode('utf-8')))

start_time = time.time()
count = 1
# cursor.execute("TRUNCATE account_move_line;")
for message in consumer:
    if message.value['key'] == 'test':
        print(message)
        username = message.value['username']
        password = message.value['password']
        # cursor.execute("INSERT INTO USERS (username,password,full_name) VALUES (%s,%s,%s)",
        #                (username, password, username))
    if message.value['key'] == 'move':
        print("Move------------")
        id = int(message.value['id']) if 'id' in message.value else 0
        ref = message.value['ref']
        credit = message.value['credit']
        debit = message.value['debit']
        sql = "INSERT INTO account_move_line (id,ref,credit,debit) VALUES ({0},'{1}','{2}','{3}')".format(id, ref,
                                                                                                          credit,
                                                                                                          debit)
        # cursor.execute(sql)

end_time = time.time()
# users = cursor.execute('SELECT * FROM users')
# for rec in users:
#     print(rec.username)
#
# print("Total Time: {0}".format(end_time - start_time))
