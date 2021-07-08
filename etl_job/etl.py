# connect to mongodb database via pymongo
import pymongo
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine

time.sleep(15) # seconds

#print("hello from the ETL container")

client = pymongo.MongoClient("mongodb")
db = client.tweets

pg = create_engine('postgres://pbamoo:1234@postgresdb:5432/mongodb')

pg.execute('''
CREATE TABLE IF NOT EXISTS tweets (
text VARCHAR(1000),
sentiment NUMERIC
);
''')

s = SentimentIntensityAnalyzer()
entries = db.tweets.find()
for e in entries:
    sentiment = s.polarity_scores(e['text'])
    print(sentiment)
    text = e['text']
    text = text.replace("'", " ")
    score = sentiment['compound']
    query = f"INSERT INTO tweets VALUES ('{text}', {score});"
    pg.execute(query)
    #pg.execute(f"""INSERT INTO tweets VALUES ('{text}', {sentiment});""")
