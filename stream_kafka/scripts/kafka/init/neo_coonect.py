from neo4j import GraphDatabase
import utils
import psycopg2

pg = utils.DbConnect('postgres')
driver = GraphDatabase.driver("bolt://192.168.56.22:7687")


def add_friend(tx, branch, user):
    tx.run("MERGE (a:Branch {name: $branch}) "
           "MERGE (a)-[:KNOWS]->(user:User {name: $user})",
           branch=branch, user=user)


def print_friends(tx, name):
    for record in tx.run("match (n) return n"):
        print(record)


connection = psycopg2.connect(user=pg['username'], password=pg['password'], host=pg['hostname'], port=pg['port'],
                              database=pg['database'])
cursor = connection.cursor()
cursor.execute("SELECT ou.name,ru.login from res_users ru \
                LEFT JOIN operating_unit ou \
                ON (ou.id = ru.default_operating_unit_id) \
                WHERE ou.name IS NOT NULL \
                ORDER BY ou.name DESC;")

with driver.session() as session:
    for val in cursor.fetchall():
        print("User Name:{0}, Branch: {1}".format(val[0], val[1]))
        session.write_transaction(add_friend, val[0], val[1])

driver.close()
