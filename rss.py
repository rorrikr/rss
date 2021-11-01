import sys
#import urllib3
#import certifi
import sqlite3
import smtplib
import feedparser
from email.mime.text import MIMEText

def read_store_article_feed():
    #Get articles from RSS feed
    feed = feedparser.parse('https://fedoramagazine.org/feed/')
    for article in feed['entries']:
        if article_is_not_db(article['title'], article['published']):
            ### Email notification
            #send_notification(article['title'], article['link'])
            ### Telegram notification
            #send_telegram_notification(article['title'], article['link'])
            add_article_to_db(article['title'], article['published'])


db_connection = sqlite3.connect('/var/tmp/magazine_rss.sqlite')
db = db_connection.cursor()
db.execute('CREATE TABLE IF NOT EXISTS magazine (title TEXT, date TEXT)')
if __name__ == '__main__':
    read_store_article_feed()
    db_connection.close()
