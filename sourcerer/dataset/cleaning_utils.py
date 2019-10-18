from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import pandas as pd

def lower_case(article):
    return [word.lower() for word in article]

def remove_stop_words(article):
    stopword_set = set(stopwords.words('english'))
    return [word for word in article if word not in stopword_set]

def remove_non_alpha(article_tokens):
    return [word for word in article_tokens if any(c.isalpha() for c in word)]

def get_article_word_count(article, domain_name, url, min_count=2):
    tokens = word_tokenize(article)
    alpha_tokens = remove_non_alpha(tokens)
    cleaned_tokens = remove_stop_words(alpha_tokens)
    cleaned_tokens = lower_case(cleaned_tokens)
    all_words = pd.Series(cleaned_tokens)
    word_counts = all_words.value_counts()

    filtered_words = word_counts[word_counts >= min_count]
    filtered_words["_URL_"] = url
    filtered_words["_SOURCE_"] = domain_name

    return filtered_words

def get_article_word_counts(articles_df, min_count=2):
    counts_df = articles_df.apply(
        lambda row: get_article_word_count(
            row["articles"],
            row["domain_name"],
            row["url"],
            min_count
        ), axis=1
    )
    counts_df = counts_df.fillna(0)
    return counts_df

def get_word_freqs(articles, min_word_count=2):

    word_counts = get_domain_word_count(articles)
    filtered_word_counts = filter_word_count(word_counts, min_word_count)

    total_words = sum(filtered_word_counts.values())
    normalized_word_freqs = {k:float(v)/total_words for k,v in filtered_word_counts.iteritems()}
    return normalized_word_freqs
