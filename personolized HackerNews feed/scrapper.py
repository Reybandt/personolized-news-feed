import requests
import re
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    cols = parser.findAll('table')[2]
    rows = cols.findAll('tr')
    for i in range(0, 90, 3):
        voc = {'title': rows[i].find('a', class_='storylink').text}

        try:
            voc['author'] = rows[i + 1].find('a', class_='hnuser').text
        except:
            voc['author'] = 'No author'

        try:
            voc['url'] = rows[i].find('span', class_='sitestr').text
        except:
            voc['url'] = 'No url'

        try:
            voc['comments'] = int(rows[i + 1].findAll('a')[3].text.split()[0])
        except:
            voc['comments'] = 'No comments'
        
        try:
            voc['points'] = int(rows[i + 1].span.text.split()[0])
        except:
            voc['points'] = 'No points'
        news_list.append(voc)
    return news_list
    

def extract_next_page(parser):
    """ Extract next page URL """
    rows = parser.findAll('table')[2].findAll('tr')
    next_page = rows[-1].a['href']
    return next_page


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
    