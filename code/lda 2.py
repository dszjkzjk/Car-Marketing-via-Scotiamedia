#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:02:48 2019

@author: junkangzhang
"""
import numpy as np
import pandas as pd
import ast
import lda
from nltk.tokenize import PunktSentenceTokenizer, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


df = pd.read_csv('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/google_tags.csv')
#df = df.drop('Unnamed: 0.1',axis=1)

######################
## make '[]' []
google_individual_tags_lst = []
for lst in df['google_api']:
    lst = ast.literal_eval(lst)
    lst = [n.strip() for n in lst]
    google_individual_tags_lst.append(lst)

df = df.drop('google_api',axis=1)
df.insert(loc=3, column='google_api', value=google_individual_tags_lst)

## make [] ' '
google_individual_tags_modi = []
for i in df['google_api']:
    string = ''
    for item in i:
        add = item + ' '
        string += add
    google_individual_tags_modi.append(string)


df['google_individual_tags_modi'] = google_individual_tags_modi
#df = df[df.google_individual_tags_modi != '']

word_tokenizer=RegexpTokenizer(r'\w+')
wordnet_lemmatizer = WordNetLemmatizer()
stopwords_nltk=set(stopwords.words('english'))

def tokenize_text(version_desc):
    lowercase=version_desc.lower()
    tokens = word_tokenizer.tokenize(lowercase)
    return tokens

vec_words = CountVectorizer(tokenizer=tokenize_text,stop_words=stopwords_nltk,decode_error='ignore')
total_features_words = vec_words.fit_transform(df['google_individual_tags_modi'])

print(total_features_words.shape)

ntopics = 5
model = lda.LDA(n_topics=int(ntopics), n_iter=500, random_state=1)
model.fit(total_features_words)

topic_word = model.topic_word_ 
doc_topic=model.doc_topic_
doc_topic=pd.DataFrame(doc_topic)
df=df.join(doc_topic)

topics=pd.DataFrame(topic_word)
topics.columns=vec_words.get_feature_names()
topics1=topics.transpose()
#topics1.to_excel("topic_word_dist.xlsx")
#df_lda.to_excel("df_lda_topic_dist.xlsx",index=False)


topic_dist = pd.DataFrame()
for i in range(5):
    lst = topics1.sort_values(i,ascending=False).index[0:10]
    topic_dist['topic '+str(i)] = lst

# engagement score
max_likes = max(df['likes'])
max_comments = max(df['comments'])
max_retweets = max(df['retweets'])
df['engagement'] = df['likes']/max_likes*0.5 + df['comments']/max_comments*0.3 + df['retweets']/max_retweets*0.2

# take the highest and the lowest quartiles (by engagement score)
df_partc = df[['id','user_name','engagement',0,1,2,3,4]]
top_25percent = df_partc.sort_values('engagement',ascending=False).iloc[0:int(len(df)*0.25),:]
bottom_25percent = df_partc.sort_values('engagement',ascending=False).iloc[int(len(df)*0.75):,:]

# rename
colnames = ['id','user_name','engagement','racing&tech','cars','car design','wildlife','design']
top_25percent.columns = colnames
bottom_25percent.columns = colnames

top_25percent.to_csv('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/top.csv')
bottom_25percent.to_csv('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/bottom.csv')

