from sourcerer.dataset.cleaning_utils import get_article_word_counts
from sourcerer.scraper.article_persistence import read_articles
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt

article_df = read_articles(["nyt", "wire", "jacobin", "cnn", "wsj", "msnbc"], "./data/dev")
count_df = get_article_word_counts(article_df)

# aggregate
agg_count_df = count_df.drop(labels=["_URL_"], axis=1)
agg_count_df = agg_count_df.groupby("_SOURCE_").sum()
agg_count_df = agg_count_df.apply(lambda source: source/source.sum(), axis=1)
agg_count_df = agg_count_df.transpose()

# pairwise distances
pd.DataFrame(
    squareform(pdist(agg_count_df.transpose())),
    index=agg_count_df.columns,
    columns= agg_count_df.columns
)


# PCA
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def plot_source_cluster(source, target, principal_df, color, alpha=0.5):
    indicesToKeep = target == source
    plt.scatter(
        principal_df.loc[indicesToKeep, 'pc1'],
        principal_df.loc[indicesToKeep, 'pc2'],
        c=color,
        s=10,
        alpha=alpha
    )

def plot_2d_pca(
        features,
        target,
        x_lims=None,
        y_lims=None,
        alpha=0.5
):
    x = features.values
    scaled_x = StandardScaler().fit_transform(x)
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(scaled_x)
    principalDf = pd.DataFrame(
        data=principalComponents,
        columns=['pc1', 'pc2']
    )
    unique_targets = list(target.unique())
    for target_name in unique_targets:
        plot_source_cluster(target_name, target, principalDf, np.random.rand(3,), alpha)
    plt.legend(unique_targets)
    if x_lims:
        plt.xlim(x_lims)
    if y_lims:
        plt.ylim(x_lims)
    plt.show()


# plot all articles
plot_2d_pca(
    count_df.drop(columns=["_URL_", "_SOURCE_"]),
    count_df["_SOURCE_"],
    x_lims=(-100,100),
    y_lims=(-100,100)
)


plot_2d_pca(
    count_df.drop(columns=["_URL_", "_SOURCE_"]),
    count_df["_SOURCE_"],
    x_lims=(-1,1),
    y_lims=(-1,1)
)


# plot sources
agg_count_df_t = agg_count_df.transpose()
plot_2d_pca(
    agg_count_df_t,
    agg_count_df_t.index
)