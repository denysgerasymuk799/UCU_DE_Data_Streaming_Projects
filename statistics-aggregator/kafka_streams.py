import json
import faust
import logging
import time

from logger import CustomHandler
from config import *


# Prepare own helper class objects
logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(CustomHandler())


# Initialize Faust app along with Kafka topic objects.
app = faust.App('statistics-aggregator',
                broker=KAFKA_BROKER,
                value_serializer='raw',
                web_host=FAUST_HOST,
                web_port=FAUST_PORT)
languages_topic = app.topic(LANGUAGES_TOPIC, partitions=3)
langs_table = app.Table("langs-count", key_type=str, value_type=int, partitions=3, default=int)

sentiments_topic = app.topic(SENTIMENTS_TOPIC, partitions=3)
sentiments_table = app.Table("sentiments-count", key_type=str, value_type=int, partitions=3, default=int)


@app.agent(languages_topic)
async def process_languages(languages):
    i = 0
    async for record in languages:
        # Get message details
        message = json.loads(record)
        langs_table[message['language']] += 1
        i += 1
        if i % 10 == 0:
            print(langs_table.as_ansitable(title='Languages Table'))


@app.agent(sentiments_topic)
async def process_sentiments(sentiments):
    i = 0
    async for record in sentiments:
        # Get message details
        message = json.loads(record)
        sentiments_table[message['sentiment']] += 1
        i += 1
        if i % 10 == 0:
            print(sentiments_table.as_ansitable(title='Sentiments Table'))
