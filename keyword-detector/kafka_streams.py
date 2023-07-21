import json
import faust
import logging

from summa import keywords
from logger import CustomHandler
from config import *


# Prepare own helper class objects
logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(CustomHandler())

# Initialize Faust app along with Kafka topic objects.
app = faust.App('keyword-detector',
                broker=KAFKA_BROKER,
                value_serializer='raw',
                web_host=FAUST_HOST,
                web_port=FAUST_PORT)
comments_topic = app.topic(COMMENTS_TOPIC)
keywords_topic = app.topic(KEYWORDS_TOPIC)


@app.agent(comments_topic)
async def process_comments(records):
    async for record in records:
        # Get message details
        subreddit, comment = record.decode("utf-8").split(DELIMITER)

        # Do the required stuff
        TR_keywords = keywords.keywords(comment, scores=False, split=True)
        message = {
            'subreddit': subreddit,
            'keywords': [kw.lower() for kw in TR_keywords],
        }
        await keywords_topic.send(value=json.dumps(message).encode())
