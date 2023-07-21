import json
import logging
from kafka import KafkaConsumer
from kafka import KafkaProducer
from textblob import TextBlob


DELIMITER = ";;; "
COMMENTS_TOPIC = "CommentsTopic"
SENTIMENTS_TOPIC = "SentimentsTopic"

logging.basicConfig(level=logging.INFO)


def on_send_error(exc_info):
    print(f'ERROR Producer: Got errback -- {exc_info}')


class TextAnalyzer:
    def analyze(self, text):
        analysis = TextBlob(text)
        sentiment_polarity = analysis.sentiment.polarity

        if sentiment_polarity >= 0:
            return 'Positive'
        elif sentiment_polarity < 0:
            return 'Negative'


class KafkaConsumerService:
    def __init__(self, bootstrap_servers, topic_name):
        self.consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=bootstrap_servers,
            api_version=(0, 10, 1),
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            consumer_timeout_ms=10
        )

    def consume_messages(self):
        return self.consumer


class KafkaProducerService:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            api_version=(0, 10, 1),
            acks='all',
            retries=3,
            max_in_flight_requests_per_connection=1,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    def produce_messages(self):
        return self.producer


class SentimentAnalyzerService:
    def __init__(self, kafka_producer, kafka_consumer, text_analyzer):
        self.kafka_producer = kafka_producer
        self.kafka_consumer = kafka_consumer
        self.text_analyzer = text_analyzer
        self.delimiter = DELIMITER

    def analyze_sentiment(self):
        producer = self.kafka_producer.produce_messages()
        consumer = self.kafka_consumer.consume_messages()
        while True:
            try:
                for msg in consumer:
                    subreddit, comment = msg.value.split(self.delimiter)
                    sentiment = self.text_analyzer.analyze(comment)

                    message = {
                        'subreddit': subreddit,
                        'sentiment': sentiment,
                    }
                    producer.send(SENTIMENTS_TOPIC, value=message).add_errback(on_send_error)
                    producer.flush()
            except Exception as e:
                logging.error(f'Error occurred: {e}')


if __name__ == "__main__":
    logging.info("starting..")
    text_analyzer = TextAnalyzer()
    kafka_producer = KafkaProducerService('kafka_broker1:9092')
    kafka_consumer = KafkaConsumerService('kafka_broker1:9092', COMMENTS_TOPIC)
    sentiment_service = SentimentAnalyzerService(kafka_producer, kafka_consumer, text_analyzer)
    sentiment_service.analyze_sentiment()
