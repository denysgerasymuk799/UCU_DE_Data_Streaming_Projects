import json
import faust
import logging

from config import *


logging.basicConfig(level=logging.INFO)


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

keywords_topic = app.topic(KEYWORDS_TOPIC, partitions=3)
keywords_table = app.Table("keywords-count", key_type=str, value_type=int, partitions=3, default=int)


def get_top_rows(table, top_n: int):
    top_n_vals = []
    for k, v in table.items():
        if len(top_n_vals) < top_n:
            top_n_vals.append((k, v))
            if len(top_n_vals) == top_n:
                top_n_vals = sorted(top_n_vals, key=lambda x: x[1], reverse=True)
        else:
            if v > top_n_vals[-1][1]:
                top_n_vals[-1] = (k, v)
                top_n_vals = sorted(top_n_vals, key=lambda x: x[1], reverse=True)

    return top_n_vals


@app.timer(interval=3.0)
async def every_minute():
    logging.info(f"\n{'=' * 20} List of languages with numbers of messages {'=' * 20}\n"
                 f"{langs_table.as_ansitable()}")
    logging.info(f"\n{'=' * 20} Number of messages among sentiment classes {'=' * 20}\n"
                 f"{sentiments_table.as_ansitable()}")

    top_n_vals = get_top_rows(keywords_table, top_n=10)
    final_str = ''
    for keyword, num_occurrences in top_n_vals:
        final_str += f'{keyword}: {num_occurrences}\n'
    final_str += '\n\n\n'
    logging.info(f"\n{'=' * 20} Top 10 keywords {'=' * 20}\n"
                 f"{keywords_table.as_ansitable()}\n\n{final_str}")


@app.agent(languages_topic)
async def process_languages(records):
    async for record in records:
        # Get message details
        message = json.loads(record)
        langs_table[message['language']] += 1


@app.agent(sentiments_topic)
async def process_sentiments(records):
    async for record in records:
        # Get message details
        message = json.loads(record)
        sentiments_table[message['sentiment']] += 1


@app.agent(keywords_topic)
async def process_keywords(records):
    async for record in records:
        # Get message details
        message = json.loads(record)
        for keyword in message['keywords']:
            keywords_table[keyword] += 1
