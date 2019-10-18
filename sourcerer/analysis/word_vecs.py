import pandas as pd

def build_word_vec(word_freq_dict):
    return pd.Series(word_freq_dict)


def merge_word_vecs(source_to_word_vec):
    df = pd.DataFrame(source_to_word_vec)
    df = df.fillna(0)
    return df