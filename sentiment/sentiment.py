import os

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date

import days
from scraper import scraper

app = Flask(__name__)
app.config.from_object('config')


@app.route("/")
def home():
    d = datetime.now().strftime("%B %d, %Y")
    day = days.get_entry(date.today() - timedelta(days=23))
    comment1_title = scraper.get_title(day.comment1_url)
    comment2_title = scraper.get_title(day.comment2_url)
    comment3_title = scraper.get_title(day.comment3_url)
    if day.sentiment <= -0.7:
    	mood = "Terrible &#x1F621;"
    	color = "#ff4c40"
    elif day.sentiment > -0.7 and day.sentiment <= -0.4:
    	mood = "Bad &#x1F625;"
    	color = "#ff6459"
    elif day.sentiment > -0.4 and day.sentiment <= -0.1:
    	mood = "Meh &#x1F615;"
    	color = "#ff9359"
    elif day.sentiment > -0.1 and day.sentiment <= 0.1:
    	mood = "Neutral &#x1F610;"
    	color = "#fdd835"
    elif day.sentiment > 0.1 and day.sentiment <= 0.4:
    	mood = "Fine &#x1F600;"
    	color = "#a9e66c"
    elif day.sentiment > 0.4 and day.sentiment <= 0.7:
    	mood = "Cheery &#x1F60E;"
    	color = "#50e582"
    else:
    	mood = "Ecstatic &#x1F60D;"
    	color = "#4ce659"
    return render_template('index.html',
                            date = d,
                            mood = mood,
                            header_color = color,
                            day = day,
                            comment1_title = comment1_title,
                            comment2_title = comment2_title,
                            comment3_title = comment3_title,)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")