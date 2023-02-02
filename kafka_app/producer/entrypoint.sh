#!/bin/sh

echo "Waiting for kafka..."

while ! kafkacat -b $KAFKA_HOST:$KAFKA_PORT -L;
do
  sleep 0.1
  echo "waiting"
done

echo "Kafka started"

exec "$@"