# !/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

seoul_data = pd.read_csv('model\seoul_attractions.csv')

metaData = seoul_data[['분류', '고유번호', '상호명', 'TAG']].drop_duplicates()
metaData.columns = ['category', 'id', 'name', 'tag']
metaData['tag'] = metaData['tag'].map(lambda x: x.replace(',', ' '))

# Content-Based Recommender - TAG 기반 추천
# TF-IDF
tfidf = TfidfVectorizer(max_features=100, max_df=0.95, min_df=0)
tfidf_matrix = tfidf.fit_transform(metaData['tag'])

# 코사인유사도
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(metaData.index, index=metaData['name']).drop_duplicates()  # 이름, index


def get_recommendations(name, cosine_sim=cosine_sim):


    if not name in indices:
        print('[ {} ]가 데이터셋에 없습니다 - KeyError'.format(name))
        return None

    idx = indices[name]
    sim_scores = list(enumerate(cosine_sim[idx]))  # 유사도 측정
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # 내림차순

    sim_scores = sim_scores[1:12]
    attraction_indices = [i[0] for i in sim_scores]

    # name 값들 얻어오기
    result = metaData[['name']].iloc[attraction_indices]
    result = np.array(result.values.tolist())
    result = np.delete(result, 1)  # 2차원 --> 1차원
    return result


### 카테고리, TAG를 고려한 CBF
def create_soup(x):
    return x['category'] + ' ' + x['tag']


metaData['soup'] = metaData.apply(create_soup, axis=1)

# TF-IDF 대신 CountVectorizer
count = CountVectorizer()
count_matrix = count.fit_transform(metaData['soup'])

# 코사인 유사도 구하기
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# index 초기화
metaData = metaData.reset_index()
indices = pd.Series(metaData.index, index=metaData['name'])


# target : 원하는 장소, recommendations : 추천장소 10개 list
# target = "경복궁"
# recommendations = get_recommendations(target, cosine_sim2)
# print(recommendations)
# print("size : ", len(recommendations))


def return_recommendations(target):
    expected_recommendations = get_recommendations(target, cosine_sim2)
    return expected_recommendations

