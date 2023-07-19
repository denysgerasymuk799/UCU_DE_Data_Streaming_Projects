import json
import faust
import logging

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
languages_topic = app.topic(LANGUAGES_TOPIC)
langs_table = app.Table("langs-count", key_type=str, value_type=int, partitions=3, default=int)


@app.agent(languages_topic)
async def process_languages(records):
    i = 0
    async for record in records:
        # Get message details
        message = json.loads(record)
        langs_table[message['language']] += 1
        i += 1
        if i % 10 == 0:
            print(langs_table.as_ansitable(title='Languages Table'))
