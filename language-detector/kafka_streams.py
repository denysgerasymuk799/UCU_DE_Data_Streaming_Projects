import json
import faust
import logging

from langdetect import detect, DetectorFactory
from logger import CustomHandler
from config import *


DetectorFactory.seed = 0

# Prepare own helper class objects
logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(CustomHandler())


# Initialize Faust app along with Kafka topic objects
app = faust.App('language-detector',
                broker=KAFKA_BROKER,
                value_serializer='raw',
                web_host=FAUST_HOST,
                web_port=FAUST_PORT)
comments_topic = app.topic(COMMENTS_TOPIC)
languages_topic = app.topic(LANGUAGES_TOPIC)


@app.agent(comments_topic)
async def process_comments(records):
    async for record in records:
        # Get message details
        subreddit, comment = record.decode("utf-8").split(DELIMITER)

        # Do the required stuff
        lang = detect(comment)
        message = {
            'subreddit': subreddit,
            'language': lang,
        }
        await languages_topic.send(value=json.dumps(message).encode())
