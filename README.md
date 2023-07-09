# Project A. E2E data processing pipeline - processing social media data (reddit)

**Team**: Denys Herasymuk and Dmytro Lopushanskyy

## How to run it?

## Dataset

## Statistics

1) Prepare a datatset - reddit dataset of subreddits.
2) Prepare a kafka environment. 
3) Implement a “generator” microservice that splits the dataset to messages reddit comments, sends them to kafka as message. 
4) Implement a microservice that detects a language of a message
5) Implement a microservice that recognizes sentiment class of a message. List of sentiment classes: Negative, Positive
6) Implement a microservice that generates a keyword list of a message
7) Implement a microservice that generates and displays  a statistics :
- list of languages with numbers of messages
- number of messages among sentiment classes 
- top 10 keywords
