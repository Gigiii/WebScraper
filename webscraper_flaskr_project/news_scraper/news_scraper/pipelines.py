import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from news_scraper.keyword_filter import processKeywords
import pandas as pd
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

#Create the engine and session to communicate with SQLite database through SQLAlchemy
engine = create_engine('sqlite:///WebScraper.db')
Session = sessionmaker(bind=engine)
metadata = MetaData()
session = Session()

#Processes the titles item sent from the spiders in news_spiders
class NewsScraperPipeline:

    def process_item(self, item, spider):


        #process item into keywords and return a dataframe
        new_keywords = processKeywords(item['titles'])

        #read existing keywords and merge them with the new ones to increase the count
        existing_keywords = pd.read_sql_table('keywords', engine)
        merged_keywords = pd.merge(existing_keywords, new_keywords,on='keyword', how='outer')
        merged_keywords['count'] = (merged_keywords['count_x'].fillna(0) + merged_keywords['count_y'].fillna(0)).astype('int')

        # Drop unnecessary columns
        merged_keywords = merged_keywords.drop(['count_x', 'count_y'], axis=1)

        #Insert dataframe into the database
        merged_keywords.to_sql('keywords', con=engine, if_exists='replace', index=False)

        #Commit the changes
        session.commit()
