from article import Article
from db import session, Base, engine
from datetime import date

Base.metadata.create_all(engine)

article1 = Article(country='Britain',
                   publication_name='British Times',
                   headlines='Britain sucks :(',
                   retrieval_date=date.fromisoformat('2023-12-03'))

session.add(article1)
session.commit()

found_article = session.query(Article).filter_by(country='Britain').first()
print(found_article.publication_name)