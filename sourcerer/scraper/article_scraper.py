import time

from nltk.tokenize import sent_tokenize, word_tokenize

from sourcerer.scraper.bs_utils import get_soup


def remove_non_alpha(paragraphs):
    return [[word for word in para if any(c.isalpha() for c in word)] for para in paragraphs]

def get_paragraph_token_len(paragraph):
    tokens = word_tokenize(paragraph)
    alpha_tokens = remove_non_alpha(tokens)
    return len(alpha_tokens)

def remove_short_paragraphs(paragraphs, min_num_tokens=10):
    paragraphs_and_len = [(para, get_paragraph_token_len(para)) for para in paragraphs]

    return [para for para, length in paragraphs_and_len if length >= min_num_tokens]


def filter_non_article_paragraphs(paragraphs):

    article_paragraph_lists = remove_short_paragraphs(paragraphs)

    return article_paragraph_lists


def get_article_string(article_url):
    article = get_soup(article_url)
    paragraphs = [para.get_text() for para in article.find_all('p')]

    article_paragraphs = filter_non_article_paragraphs(paragraphs)
    article_string = " ".join(article_paragraphs)
    return article_string

def get_article_strings(article_urls, sleep=0):
    url_to_article = {}
    for url in article_urls:
        try:
            url_to_article[url] = get_article_string(url)
            time.sleep(sleep)
        except Exception as e:
            pass

    return url_to_article


