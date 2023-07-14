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
app = faust.App('language-detector',
                broker=KAFKA_BROKER,
                value_serializer='raw',
                web_host=FAUST_HOST,
                web_port=FAUST_PORT)
comments_topic = app.topic(COMMENTS_TOPIC)
languages_topic = app.topic(LANGUAGES_TOPIC)


@app.agent(comments_topic)
async def process_transactions(records):
    async for record in records:
        # Get message details.
        subreddit, comment = record.split(DELIMITER)
        # Log received message.
        logger.info(f"subreddit: {subreddit}. comment: {comment[:50]}.")

        # Do the required stuff.
