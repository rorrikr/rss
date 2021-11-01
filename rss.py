import sys
import urllib3
import certifi
import sqlite3
import feedparser


db_connection = sqlite3.connect('db.sqlite')
db = db_connection.cursor()
db.execute('CREATE TABLE IF NOT EXISTS magazine (title TEXT, date TEXT)')


def send_telegram_notification(article_title, article_url):

    bot_id = 'token'
    chat_id = 'id'

    try:
        https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        r = https.request('GET', 'https://api.telegram.org/bot'
                        + bot_id + '/sendMessage?chat_id='
                        + chat_id + '&text=' + article_title + article_url)
    except urllib3.exceptions.SSLError as err:
        print('[ERROR] Telegram SSL error', err)
        sys.exit()

def article_is_not_db(article_title, article_date):
    db.execute("SELECT * from magazine WHERE title=? AND date=?", (article_title, article_date))
    if not db.fetchall():
        return True
    else:
        return False

def add_article_to_db(article_title, article_date):
    db.execute("INSERT INTO magazine VALUES (?, ?)", (article_title, article_date))
    db_connection.commit()

def read_store_article_feed():
    """ Get articles from RSS feed """
    feed = feedparser.parse('https://fedoramagazine.org/feed/')
    for article in feed['entries']:
        if article_is_not_db(article['title'], article['published']):
            ### Telegram notification
            send_telegram_notification(article['title'], article['link'])
            add_article_to_db(article['title'], article['published'])


if __name__ == '__main__':
    read_store_article_feed()
    db_connection.close()