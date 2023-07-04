# Project A. E2E data processing pipeline - processing social media data (reddit)

**Team**: Denys Herasymuk and Dmytro Lopushanskyy

## How to run it?



## Dataset


## Statistics

Prepare a datatset - reddit dataset of subreddits.
Prepare a kafka environment. 
Implement a “generator” microservice that splits the dataset to messages reddit comments, sends them to kafka as message. 
Implement a microservice that detects a language of a message
Implement a microservice that recognizes sentiment class of a message. List of sentiment classes: Negative, Positive
Implement a microservice that generates a keyword list of a message
Implement a microservice that generates and displays  a statistics :
                   - list of languages with numbers of messages
                   - number of messages among sentiment classes 
                   - top 10 keywords



