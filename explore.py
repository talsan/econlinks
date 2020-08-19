import pandas as pd
import numpy as np

from gensim.parsing.preprocessing import remove_stopwords
from gensim import corpora
from gensim import models
from gensim.utils import simple_preprocess
from gensim import similarities
from gensim.parsing.porter import PorterStemmer

import pyLDAvis
import pyLDAvis.gensim


# -------------------------------------------------------------------------------
# READ RAW DATA
# -------------------------------------------------------------------------------
# get list of quarterly calls (events) generated from download_transcripts.py
calls_raw = pd.read_csv('./extracts/foolcalls_extract_20200814.csv')

# only calls from 2019
calls_raw = calls_raw.loc[calls_raw['fiscal_period_year'] == 2019, ]

# remove statement_types that are either unknown or operator (i.e. keeping P, Q, A)
calls_raw = calls_raw.loc[calls_raw['statement_type'].isin(['P'])]

# -------------------------------------------------------------------------------
# PRE PROCESSING
# -------------------------------------------------------------------------------

# new column describing each company
calls_raw['ticker_name'] = calls_raw['ticker'] + ': ' + calls_raw['company_name']

# remove nan
calls_raw = calls_raw.dropna(subset=['text'])

# join text by ticker (i.e. combine individual statements from the same call and combine calls from quarters/years)
calls = calls_raw.loc[:, ['ticker_name','text']].groupby(['ticker_name'])['text'].apply(lambda x: ''.join(x)).reset_index()

# tokenize and remove punctuation
calls['text'] = calls['text'].apply(lambda x: simple_preprocess(x, min_len=2, max_len=15, deacc=True))

# Build the bigram model
bigram = models.Phrases(calls['text'], min_count=5, threshold=100) # higher threshold fewer phrases.
bigram_model = models.phrases.Phraser(bigram)
calls['text'] = calls['text'].apply(lambda x: bigram_model[x])

# remove stopwords
calls['text'] = calls['text'].apply(lambda x: remove_stopwords(x.lower()))

# stemming (porter)
p = PorterStemmer()
calls['text'] = p.stem_documents(calls['text'])

# create dictionary object
dictionary = corpora.Dictionary(calls['text'])

# filter extremes
dictionary.filter_extremes(no_below=2, no_above=0.5)

# bag-of-words transformation
corpus = [dictionary.doc2bow(text) for text in calls['text']]

# tfidf transformation
tfidf = models.TfidfModel(corpus)  # fit model
corpus_tfidf = tfidf[corpus]  # apply model

# -------------------------------------------------------------------------------
# LSI MODEL TRANSFORMATIONS & DOCUMENT SIMILARITY
# -------------------------------------------------------------------------------

# lsi transformation
lsi_model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)  # initialize an LSI transformation
corpus_lsi = lsi_model[corpus_tfidf]  # apply model
for t in lsi_model.show_topics(): # print topics
    print(t)

# cosine similarity matrix with lsi
index_lsi = similarities.MatrixSimilarity(corpus_lsi)
sims_lsi = index_lsi[corpus_lsi]

# get top 10 peers for each ticker
n = len(sims_lsi)
for i, s in enumerate(sims_lsi):
    print(calls['ticker_name'].iloc[i])
    print(calls['ticker_name'].iloc[s.argsort()[::-1][:n][0:10]])

# get top peers for each ticker
peers_lsi = pd.DataFrame()
for i, s in enumerate(sims_lsi):
    peers_idx = np.where(s > 0.80)[0].tolist()
    this_df = pd.DataFrame({'company': [calls['ticker_name'].iloc[i]]*len(peers_idx),
                            'peer': calls['ticker_name'].iloc[peers_idx],
                            'value': s[peers_idx]})
    peers_lsi = pd.concat([peers_lsi, this_df])

peers_lsi.to_csv('output/peers_lsi.csv',sep='|',index=False)


# -------------------------------------------------------------------------------
# LDA MODEL TRANSFORMATIONS & DOCUMENT SIMILARITY
# -------------------------------------------------------------------------------

# lda transformation
lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
corpus_lda = lda[corpus] # apply lda model to corpus
lda.print_topics()

# data visualization
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
vis

# cosine similarity matrix with lda
index_lda = similarities.MatrixSimilarity(corpus_lda)
sims_lda = index_lda[corpus_lda]

# get top 10 peers for each ticker
n = len(sims_lda)
for i, s in enumerate(sims_lda):
    print(calls['ticker_name'].iloc[i])
    print(calls['ticker_name'].iloc[s.argsort()[::-1][:n][0:10]])

# get top peers for each ticker
peers_lda = pd.DataFrame()
for i, s in enumerate(sims_lda):
    peers_idx = np.where(s > 0.975)[0].tolist()
    this_df = pd.DataFrame({'company': [calls['ticker_name'].iloc[i]]*len(peers_idx),
                            'peer': calls['ticker_name'].iloc[peers_idx],
                            'value': s[peers_idx]})
    peers_lda = pd.concat([peers_lda, this_df])

# get additional data
# etf holdings
# market cap