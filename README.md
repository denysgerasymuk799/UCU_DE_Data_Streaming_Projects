# Project A. E2E data processing pipeline - processing social media data (reddit)

**Team**: Denys Herasymuk and Dmytro Lopushanskyy

## Dataset

1 million Reddit comments from 40 subreddits:
https://www.kaggle.com/datasets/smagnan/1-million-reddit-comments-from-40-subreddits

Please download the dataset and place it to `./generator/data/kaggle_RC_2019-05.csv`.


## How to run it?

Execute the following command in the root of the project:
```shell
./UCU_DE_Data_Streaming_Projects$ docker-compose up --build
```

## Tasks

1) Prepare a dataset - reddit dataset of subreddits.
2) Prepare a kafka environment. 
3) Implement a “generator” microservice that splits the dataset to messages reddit comments, sends them to kafka as message. 
4) Implement a microservice that detects a language of a message.
5) Implement a microservice that recognizes sentiment class of a message. List of sentiment classes: Negative, Positive.
6) Implement a microservice that generates a keyword list of a message.
7) Implement a microservice that generates and displays a statistics:
   - list of languages with numbers of messages
   - number of messages among sentiment classes 
   - top 10 keywords


## Notes

* Note that there is no framework in Python that supports Kafka Streams aggregations. Therefore, to get top 10 keywords, statistics-aggregator finds top 10 records with the greatest numbers of occurrences each time.
For that it reads all records from the RocksDB table using the Faust table feature -- `table.items()`. 
If we look at [the source code](https://github.com/robinhood/faust/blob/master/faust/stores/rocksdb.py#L414) in the Faust repo, we can notice that `table.items()` works as a simple iterator, thus it does not cause any memory overflow.

* Generator service adds 200 reddits each 5 seconds to a CommentsTopic, while statistics-aggregator recomputes statistics also each 5 seconds and prints it to the terminal.
You can find sample screenshots below:

Log with statistics 1:

![stats-log1](https://github.com/denysgerasymuk799/UCU_DE_Data_Streaming_Projects/assets/42843889/aaef3c2a-1ecc-4faf-b86d-0f544289d7cb)

Log with statistics 2:

![stats-log2](https://github.com/denysgerasymuk799/UCU_DE_Data_Streaming_Projects/assets/42843889/ff667b29-6a86-4182-ac4c-15d3cc92bd4a)

Log with statistics 3:

![stats-log3](https://github.com/denysgerasymuk799/UCU_DE_Data_Streaming_Projects/assets/42843889/8c4435b9-ec90-4200-addb-cea1527b61fe)
