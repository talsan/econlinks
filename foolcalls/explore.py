import pandas as pd
from gensim.parsing.preprocessing import remove_stopwords
from gensim import corpora
from gensim import models
from gensim.summarization.textcleaner import tokenize_by_word
from gensim import similarities

# get list of quarterly calls (events) generated from download_transcripts.py
calls_raw = pd.read_csv('./extracts/foolcalls_extract_20200814.csv')

# remove nan
calls_raw = calls_raw.dropna(subset=['text'])

# remove statement_types that are either unknown or operator (i.e. keeping P, Q, A)
calls_raw = calls_raw.loc[~calls_raw['statement_type'].isin(['O', 'U'])]

# join text by ticker (i.e. combine individual statements from the same call and combine calls from quarters/years)
calls = calls_raw.loc[:, ['ticker', 'text']].groupby(['ticker'])['text'].apply(lambda x: ''.join(x)).reset_index()

# remove stopwords
calls['text'] = calls['text'].apply(lambda x: remove_stopwords(x.lower()))

# tokenize
calls['text'] = calls['text'].apply(lambda x: [w for w in tokenize_by_word(x)])

# remove words that appear only once and words that are only 1 letter long
# frequency = defaultdict(int)
# for text in calls_raw['text']:
#     for token in text:
#         frequency[token] += 1
#
# calls_raw['text'] = [
#     [token for token in token_list if ((frequency[token] > 1) and (len(token) > 1))]
#     for token_list in calls_raw['text']
# ]

# create dictionary object
dictionary = corpora.Dictionary(calls['text'])

# filter extremes
dictionary.filter_extremes(no_below=2, no_above=0.99)

# bag-of-words transformation
corpus = [dictionary.doc2bow(text) for text in calls['text']]

# tfidf transformation
tfidf = models.TfidfModel(corpus) # fit model
corpus_tfidf = tfidf[corpus] # apply model

# lsi transformation
lsi_model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)  # initialize an LSI transformation
corpus_lsi = lsi_model[corpus_tfidf] # apply model

# cosine similarity matrix
index = similarities.MatrixSimilarity(corpus_lsi)
sims = index[corpus_lsi]

# print topics
for t in lsi_model.show_topics():
    print(t)

# get top 10 peers for each ticker
n = len(sims)
for i,s in enumerate(sims):
    print(calls['ticker'].iloc[i])
    print(calls['ticker'].iloc[s.argsort()[::-1][:n][0:10]])