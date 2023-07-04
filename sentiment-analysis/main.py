from kafka import KafkaConsumer
from textblob import TextBlob
import json
import logging

logging.basicConfig(level=logging.INFO)


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


class SentimentAnalyzerService:
    def __init__(self, kafka_service, text_analyzer):
        self.kafka_service = kafka_service
        self.text_analyzer = text_analyzer
        self.delimiter = ";;; "

    def analyze_sentiment(self):
        consumer = self.kafka_service.consume_messages()
        while True:
            try:
                for msg in consumer:
                    subreddit, comment = msg.value.split(self.delimiter)
                    sentiment = self.text_analyzer.analyze(comment)
                    logging.info(f"subreddit: {subreddit}. comment: {comment[:50]}. Sentiment: {sentiment}")
            except Exception as e:
                logging.error(f'Error occurred: {e}')


if __name__ == "__main__":
    logging.info("starting..")
    kafka_service = KafkaConsumerService('kafka_broker1:9092', 'reddit_comments_topic-2')
    text_analyzer = TextAnalyzer()
    sentiment_service = SentimentAnalyzerService(kafka_service, text_analyzer)
    sentiment_service.analyze_sentiment()
