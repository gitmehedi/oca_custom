# Kafka

## Installation
### Python Code Preparation
#### Prerequitesite

Install Python and its related packages
```
- update os
$ sudo apt-get update -y

- install pre-requisite software
$ sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget -y

- install pip 
$ apt install python3-pip

```

Install Kafka on top of python

```
$ pip3 install kafka-python
```


### Configure Zoookeeper

```
- run kafka service
$ kafka/bin/kafka-server-start.sh kafka/config/server-101.properties

- create kafka topics
$ kafka/bin/kafka-topics.sh --create --zookeeper 192.168.56.22:2181 --partitions 3 --replication-factor 3 --topics numtest


```

### Reference:
* https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1
* https://pypi.org/project/kafka-python/
* https://kafka-python.readthedocs.io/en/master/


## General Cassandra Query Structure

```
-- Create table account_move_line in test_keyspace
cqlsh > CREATE TABLE test_keyspace.account_move_line (
    id int PRIMARY KEY,
    ref text,
    credit text,
    debit text
);

-- Delete records from a table
cqlsh> TRUNCATE keyspace_name.table_name;

```

