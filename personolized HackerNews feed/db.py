from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapper import get_news

Base = declarative_base()

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)
s = session()
list_news = get_news(url="https://news.ycombinator.com/", n_pages=1)
for i in list_news:
	s.add(News(**i))
s.commit()