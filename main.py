import argparse
import logging
import re

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

logging.basicConfig(level=logging.INFO)

import news_page_objects as news

from common import config

logger = logging.getLogger(__name__)

is_well_formed_link = re.compile(r'https?://.+/.$')
is_root_path = re.compile(r'^/.+$')

def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info(f'Iniciando el scrape for {host}')
    homepage = news.HomePage(news_site_uid, host)
    articles = []
    for link in homepage.article_links:
        #vamos a imprimir         print(link)
        article = _fetch_articles(news_site_uid, host, linux)

        if article:
            logger.info('Articulo extraido :v')
            articles.append(article)
            print(article.title)
    print(len(articles))


def _save_articles(news_site_uid, articles):
    now = datetime.now().strftime('%Y_%m_%d')
    out_file_name = f'{news_site_uid}_{now}'



def _fetch_articles(news_site_uid, host, link):
    logger.info(f'Iniciando extracion del articluo en : {link}')

    article = None
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host,link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error en la extraccion del articulo', exc_info=False)

    if article and not article.body:
        logger.warn('Articulo Invalido. No tiene un body')
        return None
    
    return article

def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return f'{host}{link}'
    else:
        return f'{host}/{link}'




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    news_sites_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
        help = 'Los sitios de noticias que quieras Scrape',
        type = str,
        choices = news_sites_choices)
    args = parser.parse_args()
    _news_scraper(args.news_site)
