#-*- coding:utf-8 -*-

import numpy as np
import ast
import frequency_cat
import math




def tfidf_list(item_id,tfidf_item):
    '''
    查询待测商品的tfidf对应的特征值
    :param item_id:
    :param tfidf_item:
    :return:
    '''
    goodsTfidfList=''
    for goodsItem in tfidf_item:
        itemList=goodsItem.split("|")
        goods_item = itemList[0]
        if goods_item==item_id:
            goodsTfidf=itemList[1]
            goodsTfidf=goodsTfidf.replace("[",'')
            goodsTfidf=goodsTfidf.replace("]",'')
            goodsTfidf=goodsTfidf.replace(" ",'')
            goodsTfidf=ast.literal_eval(goodsTfidf)
            goodsTfidfList=goodsTfidf
    return goodsTfidfList

def cos_dist(veca,vecb):
    '''
    计算余弦值
    :param veca:
    :param vecb:
    :return:
    '''
    dist = float(np.dot(veca,vecb)/(np.linalg.norm(veca)*np.linalg.norm(vecb)))
    return dist

def S2(fcm,cos_value):
    '''
    计算S2值
    :param fcm:
    :param cos_value:
    :return:
    '''
    return cos_value * math.log((1 + fcm), math.e)

if __name__ == "__main__":
    a = frequency_cat.collocation()
    item_id = str(264)
    tfidf_item = open('./data/tfidf_item.txt', 'r')
    tfidf_item_all = tfidf_item.readlines()
    tfidfList=tfidf_list(item_id,tfidf_item_all)
    # print(tfidfList)
    match_items = 0
    for i in tfidf_item_all:
        itemList = i.split("|")
        goods_item = itemList[0]
        if goods_item != item_id:
            goodsTfidf = itemList[1]
            goodsTfidf = goodsTfidf.replace("[", '')
            goodsTfidf = goodsTfidf.replace("]", '')
            goodsTfidf = goodsTfidf.replace(" ", '')
            goodsTfidf = ast.literal_eval(goodsTfidf)
            cos_value =cos_dist(tfidfList,goodsTfidf)
            # print("余弦值"+':'+str(cos_value))
            # 余弦值大小设置
            cos_value_set = 0.1
            if cos_value>cos_value_set:
                fcm = a.cat_mat_frequency(item_id,goods_item)
                s2 = S2(fcm,cos_value)
                print('匹配商品：',goods_item,"-","S2值：",s2)

