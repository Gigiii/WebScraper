import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from news_scraper.keyword_filter import processKeywords
import pandas as pd
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# Create the engine and session to communicate with the SQLite database through SQLAlchemy
engine = create_engine('sqlite:///WebScraper.db')
Session = sessionmaker(bind=engine)
metadata = MetaData()
session = Session()

class NewsScraperPipeline:
    """
    Processes scraped news titles and updates keyword counts in an SQLite database.
    """

    def process_item(self, item, spider):
        """
        Process the scraped item and update keyword counts.

        Args:
            item (dict): The scraped item containing news titles.
            spider: The spider that generated the item.

        Returns:
            None
        """
        # Process item into keywords and return a dataframe
        new_keywords = processKeywords(item['titles'])

        # Read existing keywords and merge them with the new ones to increase the count
        existing_keywords = pd.read_sql_table('keywords', engine)
        merged_keywords = pd.merge(existing_keywords, new_keywords, on='keyword', how='outer')
        merged_keywords['count'] = (merged_keywords['count_x'].fillna(0) + merged_keywords['count_y'].fillna(0)).astype('int')

        # Drop unnecessary columns
        merged_keywords = merged_keywords.drop(['count_x', 'count_y'], axis=1)

        # Insert the dataframe into the database
        merged_keywords.to_sql('keywords', con=engine, if_exists='replace', index=False)

        # Commit the changes
        session.commit()