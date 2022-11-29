#!/bin/bash


/kafka/kafka/bin/kafka-topics.sh --create --zookeeper 192.168.56.22:2181 --partitions 3 --replication-factor 3 --topics cassandra
/kafka/kafka/bin/kafka-server-start.sh /kafka/kafka/config/server-101.properties
