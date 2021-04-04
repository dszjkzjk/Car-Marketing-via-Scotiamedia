#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:44:50 2019

@author: junkangzhang
"""

import pandas as pd

df3 = pd.read_csv('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/df3.csv')

df3 = df3[['User_name','Mention_name','Retweet_Count','followers_count','friends_count','listed_count','Degree','Betweeness','Closeness']]
newcols = ['user_name','mention_name','retweets_received','follower_count','following_count','listed_count','network_feature_1','network_feature_2','network_feature_3']
df3.columns=newcols
df_features = df3.iloc[:,2:]

from sklearn.preprocessing import StandardScaler
standardizer = StandardScaler()
df_features_std = standardizer.fit_transform(df_features)

weights = [0.07941595154520623,0.07408866130946286,0.07601531178751796,0.3421302184169534,0.07065896891229251,0.07702189193150463,0.06056245510865317]
summ = sum(weights)
weights = [w/summ for w in weights]
#weights = [0.2,0.2,0.2,0.2,0.2,0.2,0.2]

score_lst = []
for i in range(5000):
    score = 0
    for j in range(7):
        score += weights[j] * df_features_std[i,j]
    score_lst.append(score)

df3['score'] = score_lst
df_top100 = df3.groupby(['user_name'],as_index = False)['score'].mean()
top100 = df_top100.sort_values(['score'],ascending=False).iloc[0:100,:]
top100 = top100.reset_index(drop=True)

top100.to_csv('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/top100.csv')