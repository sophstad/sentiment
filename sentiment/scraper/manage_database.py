from sqlalchemy import *
from sqlalchemy.orm import *
from sentiment import db
from datetime import date
import scraper
import models


def add_entry():
    """
    Adds an entry for today. Includes today's date, the sentiment, the top
    3 comments and their associated article urls.
    :return: None
    """
    db = create_engine("sqlite:///../db/app.db", echo = False)

    metadata = MetaData(db)

    days = Table("days", metadata, autoload = True)

    daymapper = mapper(models.Day, days)

    session = Session()

    days.drop(db)

    comment_index = 0
    vote_index = 1
    url_index = 2

    num_days = 7
    urls = scraper.get_urls(num_days)
    top_comments, top_votes = scraper.scrape(urls)

    today = models.Day(sentiment = 0.5,
                       comment1=top_comments[1][comment_index],
                       comment1_url=top_comments[1][url_index],
                       comment2=top_comments[2][comment_index],
                       comment2_url=top_comments[2][url_index],
                       comment3=top_comments[3][comment_index],
                       comment3_url=top_comments[3][url_index],
                       )

    session.add(today)
    session.commit()
    session.flush()


def delete_entry(date):
    db = create_engine("sqlite:///../db/app.db", echo = False)

    metadata = MetaData(db)

    days = Table("days", metadata, autoload = True)

    session = Session()

    removal_date = session.query(models.Day).filter_by(date = date).first()

    session.delete(removal_date)
    session.commit()
    session.flush()


def main():
    add_entry()
    delete_entry(date.today())

main()