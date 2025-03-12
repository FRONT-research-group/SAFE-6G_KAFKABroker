# Kafka Microservice for SAFE-6G Cognitive Coordination

This repository implements a Kafka-based message broker as a microservice using FastAPI. The service is designed to support the SAFE-6G cognitive coordination architecture by enabling communication between various 6G trustworthiness functions (e.g., Safety, Security, Privacy, Resilience, Reliability) and AI agents.

## Table of Contents

- [Kafka Microservice for SAFE-6G Cognitive Coordination](#kafka-microservice-for-safe-6g-cognitive-coordination)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Architecture](#architecture)
    - [Kafka and Message Broker Fundamentals](#kafka-and-message-broker-fundamentals)
    - [Design Decisions](#design-decisions)
  - [API Endpoints](#api-endpoints)
    - [Publishing Messages](#publishing-messages)
    - [Consuming Messages](#consuming-messages)
  - [Usage Examples](#usage-examples)
    - [cURL Examples](#curl-examples)
      - [Publish a Message](#publish-a-message)
      - [Consume Messages](#consume-messages)
    - [Python Requests Examples](#python-requests-examples)
      - [Publishing a Message](#publishing-a-message)
      - [Consuming Messages](#consuming-messages-1)
  - [Installation and Setup](#installation-and-setup)
    - [Prerequisites](#prerequisites)
    - [Setup Instructions](#setup-instructions)

## Overview

The microservice provides two main functionalities:

1. **KafkaProducerService:** Publishes JSON-formatted messages to specific Kafka topics. Each topic corresponds to a function type (e.g., SAFETY, SECURITY).
2. **KafkaConsumerService:** Consumes messages from Kafka topics using manual offset management to ensure reliable processing. This service is designed for pull-based message retrieval.

The system is built to be modular so that each team responsible for a particular function can manage their own Kafka topic, ensuring domain isolation and facilitating independent scaling.

## Architecture

### Kafka and Message Broker Fundamentals

**Apache Kafka** is a distributed streaming platform that functions as a durable message broker. It is widely used for building real-time data pipelines and streaming apps. Key concepts include:

- **Topics:** Categories or feed names to which messages are published. In this repository, each function type (e.g., SAFETY, SECURITY) is mapped to its own topic.
- **Partitions:** Topics can be split into partitions, which allow for horizontal scaling and parallel processing.
- **Producers:** Applications that publish messages to Kafka topics.
- **Consumers:** Applications that subscribe to topics and process the published messages.
- **Consumer Groups:** A set of consumers that share the workload of processing messages from a topic. Each consumer in a group receives a subset of the partitions.

This repository’s implementation uses Kafka to decouple the cognitive coordination components from the network functions, enabling asynchronous and scalable message processing.

### Design Decisions

- **Separate Topics per Function:**  
  Each function (SAFETY, SECURITY, etc.) has its own Kafka topic, allowing different teams to manage their message flows independently. This design improves security and allows custom configurations (e.g., partitioning, retention policies) per function.

- **Manual Offset Management:**  
  Consumers are configured to manually commit offsets. This gives more control over message processing, ensuring that messages are not lost or processed multiple times, which is crucial for reliable operation in distributed systems.

- **Pull-Based API:**  
  Functions call the broker’s API to pull messages when needed. While this design is simple and effective for on-demand processing, it can be extended later with continuously running consumers if real-time processing is required.


## API Endpoints

The microservice exposes REST API endpoints via FastAPI. The two main endpoints are:

### Publishing Messages

- **Endpoint:** `/kafka/publish`
- **Method:** `POST`
- **Description:** Publishes a Kafka message to a topic based on the message's function type.

### Consuming Messages

- **Endpoint:** `/kafka/consume/{function}`
- **Method:** `GET`
- **Description:** Consumes a batch of messages from the Kafka topic corresponding to the specified function type. Supports a `limit` parameter to control the number of messages retrieved.

## Usage Examples

### cURL Examples

#### Publish a Message

```bash
curl -X POST "http://localhost:6969/kafka/publish" \
     -H "Content-Type: application/json" \
     -d '{
           "cLoTW": 0.95,
           "function": "SAFETY",
           "targetApplicationIP": "192.168.1.10",
           "IMSI": "123456789012345",
           "MSISDN": "1234567890",
           "IMEI": "490154203237518"
         }'
```

*Expected Response:*

```json
{
  "status": "Message published to topic: SAFETY"
}
```

#### Consume Messages

```bash
curl "http://localhost:6969/kafka/consume/SAFETY?limit=5"
```

*Expected Response:*

```json
{
  "messages": [
    {
      "cLoTW": 0.95,
      "function": "SAFETY",
      "targetApplicationIP": "192.168.1.10",
      "IMSI": "123456789012345",
      "MSISDN": "1234567890",
      "IMEI": "490154203237518"
    }
    // ... up to 5 messages
  ]
}
```

### Python Requests Examples

#### Publishing a Message

```python
import requests

url = "http://localhost:6969/kafka/publish"
payload = {
    "cLoTW": 0.95,
    "function": "SAFETY",
    "targetApplicationIP": "192.168.1.10",
    "IMSI": "123456789012345",
    "MSISDN": "1234567890",
    "IMEI": "490154203237518"
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

#### Consuming Messages

```python
import requests

# Consuming messages for the SAFETY function, limit of 5 messages
url = "http://localhost:6969/kafka/consume/SAFETY?limit=5"
response = requests.get(url)
print(response.json())
```

## Installation and Setup

### Prerequisites

- **Python 3.8+**
- **Apache Kafka:**  
  Make sure you have a Kafka cluster running (e.g., via Docker or a local installation). Set the `KAFKA_SERVER` environment variable if needed (default is `kafka:9092`).

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/FRONT-research-group/SAFE-6G_KAFKABroker
   cd fastapi-kafka-service
   ```

2. **Create a virtual environment and install dependencies:**

    **_NOTE:_**  System was developed using rye for package and dependency management. Check instructions [here](https://rye.astral.sh/).


   ```bash
   rye sync
   ```

3. **Run the FastAPI server:**

   ```bash
   uvicorn api.api:app --host 0.0.0.0 --port 6969
   ```

   The service will now be running at [http://localhost:6969](http://localhost:6969).