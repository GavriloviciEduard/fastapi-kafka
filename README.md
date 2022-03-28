#  Kafka PoC using FastAPI 
Both the producer and the consumer wait for Kafka to accept connections using kafkacat.
## Run and test

To start the application just run 
```
docker-compose up -d
```

To post messages for the producer access swagger 
```
http://localhost:8080/kafka_producer/docs
```

To see the messages consumed by the consumer
```
docker-compose logs consumer
```
