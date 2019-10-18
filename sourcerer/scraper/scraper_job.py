import sys
sys.path.append("/Users/harryrackmil/PycharmProjects/sourcerer")

from sourcerer.scraper.article_persistence import persist_articles
from sourcerer.scraper.source_scraper import scrape_source
import logging

logging.basicConfig(level=logging.INFO)

def scrape(name, entry_url, num_articles, sleep, persistence_root):
    if name is None:
        name = entry_url.split(".")[1]

    url_to_article = scrape_source(entry_url, num_articles, sleep=sleep)
    persist_articles(name, url_to_article, persistence_root)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--name',
        type=str,
        action="store"
    )

    parser.add_argument(
        '--entry-url',
        type=str,
        action="store"
    )

    parser.add_argument(
        '--is-prod',
        action="store_true",
        default=False
    )

    parser.add_argument(
        '--num-articles',
        type=int,
        action="store",
        default=50
    )

    parser.add_argument(
        '--sleep',
        type=int,
        action="store",
        default=0
    )

    args = parser.parse_args()

    if args.is_prod:
        root_path = "./data/prod"
    else:
        root_path = "./data/dev"

    scrape(
        args.name,
        args.entry_url,
        args.num_articles,
        args.sleep,
        root_path
    )
