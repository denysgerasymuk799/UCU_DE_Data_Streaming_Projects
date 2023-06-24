import json
import time
import logging
import pandas as pd
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)


class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file

    def load_config(self):
        with open(self.config_file) as f:
            config = json.load(f)
        return config


class RedditDataChunker:
    def __init__(self, data_file):
        self.data_file = data_file

    def load_data(self):
        reddit_comments_df = pd.read_csv(self.data_file)
        reddit_comments_df = reddit_comments_df.iloc[:, :-2]  # remove the last two columns
        return reddit_comments_df


class KafkaDataProducer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            api_version=(0, 10, 1),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all'
        )
        self.delimiter = ";;; "

    def send_data(self, topic_name, df):
        for index, row in df.iterrows():
            record = self.delimiter.join(row.astype(str))
            self.producer.send(topic_name, record)
            self.producer.flush()
            logging.info(f'Sent record #{index + 1} to Kafka')

            # Periodically add messages to a topic to check statistics
            if (index + 1) % 200 == 0:
                time.sleep(5)


if __name__ == "__main__":
    config_manager = ConfigManager('config.json')
    config = config_manager.load_config()

    data_chunker = RedditDataChunker(config['dataset_location'])
    data = data_chunker.load_data()

    data_producer = KafkaDataProducer(config['kafka_server'])
    data_producer.send_data(config['topic_name'], data)
