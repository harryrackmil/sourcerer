import logging
import time

from sourcerer.scraper.article_scraper import get_article_strings
from sourcerer.scraper.link_scraper import scrape_links_from_homepage


def scrape_source(domain, max_articles=1000, sleep=0):
    logging.info("scraping domain: {}".format(domain))
    if domain[-1] == "/":
        domain = domain[:-1]

    try:
        start_time = time.time()

        links = scrape_links_from_homepage(domain, max_articles, sleep)
        urls_to_articles = get_article_strings(links, sleep)

        end_time = time.time()
        logging.info("scraping domain {} took {} minutes".format(domain, (end_time - start_time) / 60.0))
        return urls_to_articles

    except Exception as e:
        try:
            logging.info("scraping failed with this error: {}".format(e.message))
        except Exception as e:
            logging.info("failed with unprintable error")

    return {}
