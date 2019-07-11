# -*-coding:utf-8 -*-
import math
import time
import frequency_cat

def user_time(item, ubh_line):
    '''
    查找商品购买时间以及同时间购买的其它商品
    '''
    dict_item_couple = {}
    dictMerged ={}
    for each in ubh_line:
        ubh_lineone = each.split(' ')
        if(ubh_lineone[1] == item):
            user_id = ubh_lineone[0]
            bought_day = ubh_lineone[2]
            dict1 = user_bought(user_id, bought_day, item)
            # 保存购买的其它商品ID及目录
            dictMerged.update(dict1)
    dict_item_couple[item] = dictMerged
    return dict_item_couple

def user_bought(user_id, bought_day,item1_id):
    '''
    找该用户在该天购买的其他商品并统计频次
    '''
    num_dict = {}
    for each in ubh_line:
        ubh_lineone = each.split(' ')
        if((ubh_lineone[0] == user_id)and(bought_day == ubh_lineone[2])and(ubh_lineone[1]!=item1_id)):
            match_item = ubh_lineone[1]
            user_bought_1_day_list.append(match_item)
            # 统计购买频率
            if((match_item in num_dict) and (match_item != item1_id)):
                num_dict[match_item] = num_dict[match_item]+1
            else:
                num_dict[match_item] = 1

    return num_dict

def fpm(item1,item2,dict_item1):

    item2_num = dict_item1[item1]
    if item2 in item2_num:
        return item2_num[item2]
    else:
        return 0

def S1(fpm_, fcm_):
    return fpm_*math.log((1+fcm_), math.e)


def match_dict_S1(item,user_bought_1_day_list,dict_item):
    '''
    用户同日购买异类商品算法
    '''
    a = frequency_cat.collocation()
    dict_utlimate = {}
    dict_item_s1 = {}
    for each in user_bought_1_day_list:
        # fpm值计算
        num_item = fpm(item, each, dict_item)
        # 查询类间频率fcm
        num_cat = a.cat_mat_frequency(item, each)
        # 计算S1值
        n = S1(num_item, num_cat)
        dict_item_s1[each] = n
    dict_utlimate[item] = dict_item_s1
    print(dict_utlimate)
    return dict_utlimate

def final(dict,item1_id):
    dict1 = dict[item1_id]
    print( '---------------------------------------')
    print('|final result:                        |\n|                                     |')
    dict2 = sorted(dict1.items(), key=lambda item: item[1])
    for each in dict2:
        if(each[1]!=0.0):
            print('|'+each[0]+'                              |')
    print( '---------------------------------------')

if __name__ == '__main__':
    # 取时间
    time1 = time.time()
    num_dict = {}
    user_bought_1_day_list = []
    # 导入类间搭配表
    a = frequency_cat.collocation()
    # 读取用户购买商品列表
    user_bought_history = open('./data/small_user_bought_history.txt', 'r')
    # 读取达人搭配列表
    fashion_matchsets = open('./data/dim_fashion_matchsets.txt', 'r')
    # 读取商品信息表
    dim_item = open('./data/small_dim_items.txt', 'r')
    # 用户购买记录表记录
    ubh_line = user_bought_history.readlines()
    # 达人搭配记录
    fashion_match = fashion_matchsets.readlines()
    # 商品信息表记录
    dim_all_item = dim_item.readlines()
    item_list = []
    # 取某个商品
    item1_id = str(212) #701
    dict_user_time = user_time(item1_id, ubh_line)
    # 打印结果
    final(match_dict_S1(item1_id, user_bought_1_day_list, dict_user_time),item1_id)
    # 计算花费时间
    time2 = time.time()
    print('spend time:'+str(time2 - time1))