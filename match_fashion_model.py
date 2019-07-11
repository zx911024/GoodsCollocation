#-*- coding:utf-8 -*-

import numpy as np
import ast

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

def seach_dim_fashion(goods_id):
    '''
    寻找达人搭配中对应的商品，即与待测商品可以搭配的商品
    :param goods_id:
    :return:
    '''
    result = []
    fashion_matchsets = open('./data/dim_fashion_matchsets.txt', 'r')
    fashion_matchsets_all = fashion_matchsets.readlines()
    for i in fashion_matchsets_all:
        dim_item = i.split(' ')
        dim_item_str = dim_item[1]
        if ';' in dim_item_str:
            dim_item_list = dim_item_str.split(';')
            for j in dim_item_list:
                if ','in j:
                    goods_id_list = dim_item_str.split(',')
                    if goods_id in goods_id_list:
                        result_temp = goods_id_list.remove(goods_id)
                        if result_temp:
                            result.extend(result_temp)
        else:
            if ',' in dim_item_str:
                goods_id_list=dim_item_str.split(',')
                if goods_id in goods_id_list:
                    result_temp=goods_id_list.remove(goods_id)
                    result.extend(result_temp)
    return result

if __name__ == "__main__":
    item_id = str(264)
    tfidf_item = open('./data/tfidf_item.txt', 'r')
    tfidf_item_all = tfidf_item.readlines()
    tfidfList=tfidf_list(item_id,tfidf_item_all)
    # print(tfidfList)
    match_items = []
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
            print("余弦值"+':'+str(cos_value))
            # 余弦值大小设置
            cos_value_set=0
            if cos_value>cos_value_set:
                match_items_temp=seach_dim_fashion(goods_item)
                if match_items_temp:
                    print("搭配商品：",match_items_temp)
                match_items.extend(match_items_temp)
    print("所有搭配商品：",match_items)
