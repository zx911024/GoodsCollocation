#-*- coding:utf-8 -*-

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

if __name__ == "__main__":
    # 读取商品信息表
    dim_item = open('./data/small_dim_items.txt', 'r')
    dim_all_item = dim_item.readlines()
    corpus = []
    item_id = []
    for index,i in enumerate(dim_all_item):
        j=i.split(' ')
        wordLine = j[2]
        item_id.append(j[0])
        wordLine=wordLine.replace(',',' ')
        wordLine=wordLine.replace('\n','')
        corpus.append(wordLine)
        # 调节测试模型商品数量
        if index==100:
            break
    # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer=CountVectorizer()
    # 该类会统计每个词语的tf-idf权值
    transformer=TfidfTransformer()
    tf=vectorizer.fit_transform(corpus)
    # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    tfidf=transformer.fit_transform(tf)
    # 获取词袋模型中的所有词语
    word=vectorizer.get_feature_names()
    # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    weight=tfidf.toarray()
    with open('./data/tfidf_item.txt', 'w') as tfidffile:
        for i,j in zip(weight,item_id):
            print(j,i)
            i = i.tolist()
            i = str(i)
            istr="".join(i)
            tfidffile.writelines(str(j)+"|"+i+'\n')



