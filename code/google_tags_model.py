# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 11:59:36 2019

@author: ruite
"""

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk import FreqDist
import pandas as pd
import numpy as np
from sklearn.datasets import load_digits
from sklearn.manifold import MDS
from sklearn import manifold
import matplotlib.pyplot as plt
from itertools import combinations
import ast
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from operator import itemgetter
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import classification_report

df = pd.read_csv(r'C:\Users\ruite\OneDrive - McGill University\2018 MMA\digital marketing\final project\final\google_tags.csv')

df['google_api'] = df['google_api'].apply(lambda x: ast.literal_eval(x))

#create engagement score column
max_likes = max(df['likes'])
max_comments = max(df['comments'])
max_retweets = max(df['retweets'])

df['engagement'] = 0.3*df['likes']/max_likes + 0.5*df['comments']/max_comments + 0.2*df['retweets']/max_retweets

df['google_tags'] = df['google_api'].apply(lambda x: str(x))

df['google_tags'] = df['google_tags'].apply(lambda x: x.replace('[', ''))
df['google_tags'] = df['google_tags'].apply(lambda x: x.replace(']', ''))
df['google_tags'] = df['google_tags'].apply(lambda x: x.replace(",", ''))
df['google_tags'] = df['google_tags'].apply(lambda x: x.replace("'", ''))

wnl = nltk.WordNetLemmatizer()

df['google_tags'] = df['google_tags'].str.lower()
df['google_tags'] = df.apply(lambda row: wnl.lemmatize(row['google_tags']), axis=1)


####################################################################################################
data_2 = df[['engagement', 'google_tags']]
a_2 = data_2['engagement']
p_2 = np.percentile(a_2, 30)
data_2 = data_2.assign(is_better = (data_2.engagement >= p_2))

trainset_size = int(round(len(data_2)*0.6))

X_2 = data_2.iloc[:,1]
y_2 = data_2['is_better']

X_train2 = np.array([''.join(el) for el in X_2[0:trainset_size]])
y_train2 = np.array([el for el in y_2[0:trainset_size]])

X_test2 = np.array([''.join(el) for el in X_2[trainset_size:len(X_2)]]) 
y_test2 = np.array([el for el in y_2[trainset_size:len(y_2)]]) 

test_string = str(X_train2[0])

vectorizer = TfidfVectorizer(min_df=2, 
 ngram_range=(1, 2), 
 stop_words='english', 
 norm='l2',
 analyzer = 'word')


print ("Example string: " + test_string)
print ("Preprocessed string: " + vectorizer.build_preprocessor()(test_string))
print ("Tokenized string:" + str(vectorizer.build_tokenizer()(test_string)))
print ("N-gram data string:" + str(vectorizer.build_analyzer()(test_string)))
print ("\n")

 
X_train2 = vectorizer.fit_transform(X_train2)
X_test2 = vectorizer.transform(X_test2)

nb_classifier2 = BernoulliNB().fit(X_train2, y_train2)

y_nb_predicted2 = nb_classifier2.predict(X_test2)

print(str(metrics.precision_score(y_test2, y_nb_predicted2)))

print ('The precision for this classifier is ' + str(metrics.precision_score(y_test2, y_nb_predicted2)))
print ('The recall for this classifier is ' + str(metrics.recall_score(y_test2, y_nb_predicted2)))
print ('The f1 for this classifier is ' + str(metrics.f1_score(y_test2, y_nb_predicted2)))
print ('The accuracy for this classifier is ' + str(metrics.accuracy_score(y_test2, y_nb_predicted2)))

print('\nHere is the classification report:')
print(classification_report(y_test2, y_nb_predicted2))

#simple thing to do would be to up the n-grams to bigrams; try varying ngram_range from (1, 1) to (1, 2)
#we could also modify the vectorizer to stem or lemmatize
print('\nHere is the confusion matrix:')
print(metrics.confusion_matrix(y_test2, y_nb_predicted2))

###
N = 10
vocabulary = np.array([t for t, i in sorted(vectorizer.vocabulary_.items(), key=itemgetter(1))])

topN = np.argsort(nb_classifier2.coef_[0])[-N:]
print ("\nThe top %d most informative features for topic code %s: \n%s" % (N, 'True', " ".join(vocabulary[topN])))

topN1 = np.argsort(nb_classifier2.coef_[0])[:N]
print ("\nThe top %d most informative features for topic code %s: \n%s" % (N, 'False', " ".join(vocabulary[topN1])))