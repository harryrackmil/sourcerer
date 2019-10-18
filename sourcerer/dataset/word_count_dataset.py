from sourcerer.dataset.cleaning_utils import get_article_word_count
from sourcerer.scraper.article_persistence import read_articles_from_file


class WordCountDataset:
    def __init__(self, domain_names):
        for domain_name in domain_names:

    @staticmethod
    def build_word_count_df(domain_name):
        article_df = read_articles_from_file(domain_name)
        article_df = get_article_word_count(article_df["articles"][0])