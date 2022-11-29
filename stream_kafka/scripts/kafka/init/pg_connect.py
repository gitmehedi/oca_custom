import psycopg2
from psycopg2 import Error
import utils

pg = utils.DbConnect('postgres')

try:
    connection = psycopg2.connect(user=pg['username'], password=pg['password'], host=pg['hostname'], port=pg['port'],
                                  database=pg['database'])
    cursor = connection.cursor()

    cursor.execute("SELECT name,debit,credit FROM account_move_line;")
    record = cursor.fetchall()

    for val in record:
        print("Journal Name:{0}, Debit: {1}, Credit: {2}".format(val[0], val[1], val[2]))

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("Postgresql connection is closed")
