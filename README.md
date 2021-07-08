# Week 6/12 The Data Pipeline Project
   
### Background problem / Goal:
In this project, we will build a data pipeline that collect tweets and stores them in a database, then analyze the sentiment of tweets, store the annotated tweets in a second database and build a bot to publish the best or worst sentiment for a given tweet on Slack every 10 minutes.

### Tools/Libraries Used: 
Python, Pandas, Matplotlib, Scikit-learn, Wordcloud, nltk, BeautifulSoup

### Workflow:
1. Install Docker
2. Build a data pipeline with docker-compose
3. Collect Tweets
4. Store Tweets in Mongo DB
5. Create an ETL job transporting data from MongoDB to PostgreSQL
6. Run sentiment analysis on the tweets
7. Build a Slack bot that publishes selected tweets
