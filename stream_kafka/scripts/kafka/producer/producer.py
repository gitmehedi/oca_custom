import random, string, time, psycopg2, sys, os
from json import dumps
from kafka import KafkaProducer

sys.path.append(os.path.join(os.path.dirname(__file__), '../init/'))
import utils

# pg = utils.DbConnect('postgres')

COUNT = 2
KF_IP = ['localhost:9091']
pg = {
    'username': 'odoo',
    'password': 'code200!',
    'hostname': 'localhost',
    'port': '5432',
    'database': 'MGP_KAFKA',
}

producer = KafkaProducer(bootstrap_servers=KF_IP, value_serializer=lambda x: dumps(x).encode('utf-8'))

connection = psycopg2.connect(user=pg['username'], password=pg['password'], host=pg['hostname'], port=pg['port'],
                              database=pg['database'])
cursor = connection.cursor()

cursor.execute("SELECT id,name,debit,credit FROM account_move_line;")
record = cursor.fetchall()

for val in record:
    print("Journal Name:{0}, Debit: {1}, Credit: {2}".format(val[0], val[1], val[2]))
    journal = {'key': 'move', 'id': val[0], 'ref': val[1], 'credit': str(val[2]), 'debit': str(val[3])}
    producer.send('cassandra', value=journal)

for e in range(COUNT):
    username = str(e) + ''.join(random.choice(string.ascii_letters) for i in range(5))
    password = ''.join(random.choice(string.ascii_letters) for i in range(50))
    data = {'key': 'test', 'username': username, 'password': password, 'full_name': username}
    print("-----------------------{0}".format(data))
    producer.send('cassandra', value=data)
