import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from news_scraper.keyword_filter import processKeywords
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db_manager import session, engine
import pandas as pd
#Python Debugger
import pdb
#download ipython

class NewsScraperPipeline:

    def process_item(self, item, spider):
        #process item into keywords and return a dataframe
        new_keywords = processKeywords(item['titles'])

        existing_keywords = pd.read_sql_table('keywords', engine)

        merged_keywords = pd.merge(existing_keywords, new_keywords,on='keyword', how='outer')
        print(merged_keywords)
        merged_keywords['count'] = (merged_keywords['count_x'].fillna(0) + merged_keywords['count_y'].fillna(0)).astype('int')
        print(type(merged_keywords['count'][0]))
        # Drop unnecessary columns
        merged_keywords = merged_keywords.drop(['count_x', 'count_y'], axis=1)

        #Insert dataframe into the database
        merged_keywords.to_sql('keywords', con=engine, if_exists='replace', index=False)

        #Commit the changes
        session.commit()
