import pandas as pd

SEPARATOR = "|"
WRITE_HEADER = True

def clean_string(str, bad_chars, replace_char):
    for char in bad_chars:
        str = str.replace(char, replace_char)
    return str

def clean_domain(domain_name):
    bad_chars = [".", "/"]
    return clean_string(domain_name, bad_chars, "_")

def clean_article(article):
    bad_chars = ["|", "\"", "'", "\n", "_"]
    return clean_string(article, bad_chars, " ")

def write_articles_to_file(domain_name, url_to_article, persistence_root):
    cleaned_domain = clean_domain(domain_name)
    file_path = persistence_root + "/articles/" + cleaned_domain

    articles = pd.Series(url_to_article)
    df = pd.DataFrame({"articles": articles, "domain_name":domain_name})
    df = df.reset_index()
    df = df.rename(columns={"index": "url"})

    df = df[~df.isnull().any(axis=1)]

    df["articles"] = df["articles"].apply(clean_article)

    df.to_csv(
        path_or_buf=file_path,
        sep=SEPARATOR,
        header=WRITE_HEADER,
        index=False,
        encoding="utf-8"
    )

def read_articles_from_file(domain_name, persistence_root):
    cleaned_domain = clean_domain(domain_name)
    file_path = persistence_root + "/articles/" + cleaned_domain

    df = pd.read_csv(
        file_path,
        sep=SEPARATOR,
        header=0,
        index_col=None,
        encoding="utf-8",
        lineterminator='\n'
    )

    df = df[~df.isnull().any(axis=1)]

    return df

def persist_articles(domain_name, url_to_article, persistence_root):
    write_articles_to_file(domain_name, url_to_article, persistence_root)

def read_articles(domain_names, persistence_root):
    article_df = pd.DataFrame()
    for domain_name in domain_names:
        article_df = pd.concat([article_df, read_articles_from_file(domain_name, persistence_root)])
        article_df = article_df.reset_index(drop=True)
    return article_df