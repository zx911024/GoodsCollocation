## 仅仅做研究使用
### 1.数据描述 
    【1】商品信息表，该表共三列，第一列是商品的ID，第二列是商品所属类的ID，第三列是商品的特征分词（用脱敏的数字编号表示）。
    【2】达人搭配套餐表，该表一共两列，第一列是套餐ID（无实用），第二列是搭配商品ID组合（不同类用 ”;” 隔开,同类商品用 “,”隔开）。
    【3】用户购买记录表，该表分为三列，第一列是用户ID，第二列是商品ID，第三列是购买日期。
    【4】待预测商品表，该表中都是待预测商品。
## 二、算法描述
### 1.用户同日购买异类商品
    该算法中，事先过滤与待测商品中不搭配的类（达人数据中没有出现过的类间搭配），
    这一步，我们对达人搭配套餐表【2】做了预处理，将所有搭配套餐中的同类商品用其所属类ID进行替代，
    替代生成个搭配套餐中商品所属类的搭配情况。这里要用到商品信息表【1】，在其中找到对应商品的所属类别。
    用该方法处理出来的表我们称之为类间搭配表【5】，在类间搭配表【5】中，
    输入一个类，按照每一行独立搭配的原则，查找与该类搭配的类，没有出现的类视为不与该类搭配。

   ![image](https://github.com/haodong-liu/-/blob/master/pic/3.png)

    之后输入一个商品A，在用户购买记录表【3】中搜索出所有购买过该商品A的用户与购买时间，
    再用用户ID和购买时间在用户购买记录表【3】中找该用户在该天购买的其他商品B,C,D…，
    查找过程中，过滤与A相同或者与A同类的商品。同时记录商品对（比如A与B）的同天购买次数fpm ，
    再查找商品对的类间搭配频数fcm，该频数首先要查找这两个商品所属类别（比如Ca和Cb），
    用所属类别遍历类间搭配表【5】 查找Ca和Cb类的搭配频数ｆcm 。
    这里的类间搭配频数ｆcm 代表的不同类的搭配程度，频数越大，
    我们认为这两个类Ca和Cb的搭配程度就越高，反推A与B商品的搭配可能性就越大。
    这里给出我们的对于这个模型设计的评价函数：
    S1 越大，我们认为这两个商品越搭配。
    
   ![image](https://github.com/haodong-liu/-/blob/master/pic/4.jpg)

    我们找到了与A商品同天都买的商品B,C,D,E….. 计算每一对的S1 将这些数据排序输出。
    若S1算出来为0，说明ｆcm为0，则该两个商品类Ca和Cb不搭配，推出这两个商品A与B不搭配。

### 2. TFIDF文本相似度全局搜索
    该算法中，用TF-IDF文本处理与余弦相似度匹配方法，查找与待测商品A相似但不同类的商品B,C,D….
    我们认为这些商品是可能与商品A搭配的商品。下面介绍一下TF_IDF算法，
    该算法用以评估一个商品中的一个特征值对于该商品的重要程度。
    TFIDF的主要思想是：如果某个词或短语在一篇文章中出现的频率TF高，
    并且在其他文章中很少出现，则认为此词或者短语具有很好的类别区分能力，
    适合用来分类。TFIDF实际上是：TF * IDF，TF词频(Term Frequency)，
    IDF逆向文件频率(Inverse Document Frequency)。TF表示词条在文档d中出现的频率。
    IDF的主要思想是：如果包含词条t的文档越少，也就是n越小，IDF越大，则说明词条t具有很好的类别区分能力。
    如果某一类文档C中包含词条t的文档数为m，而其它类包含t的文档总数为k，显然所有包含t的文档数n=m+k，
    当m大的时候，n也大，按照IDF公式得到的IDF的值会小，就说明该词条t类别区分能力不强。但是实际上，
    如果一个词条在一个类的文档中频繁出现，则说明该词条能够很好代表这个类的文本的特征，
    这样的词条应该给它们赋予较高的权重，并选来作为该类文本的特征词以区别与其它类文档。
    这就是IDF的不足之处. 在一份给定的文件里，词频（term frequency，TF）指的是某一个给定的词语在该文件中出现的频率。
    这个数字是对词数(term count)的归一化，以防止它偏向长的文件。
    （同一个词语在长文件里可能会比短文件有更高的词数，而不管该词语重要与否。）
    对于在某一特定文件里的词语来说，它的重要性可表示为：
    
![image](https://github.com/haodong-liu/-/blob/master/pic/5.jpg)

     以上式子中分子是该词在文件中的出现次数，而分母则是在文件中所有字词的出现次数之和。
    **逆向文件频率**（inverse document frequency，IDF）是一个词语普遍重要性的度量。
    某一特定词语的IDF，可以由总文件数目除以包含该词语之文件的数目，再将得到的商取对数得到：
![image](https://github.com/haodong-liu/-/blob/master/pic/6.jpg)

    其中|D|：语料库中的文件总数|{j : ti∈∈dj }|：包含词语的文件数目（即的文件数目）如果该词语不在语料库中，
    就会导致分母为零，因此一般情况下使用1+|{j : ti∈∈dj }|作为分母。之后相称得到TF_IDF值。
    根据我们的题目要求给出计算公式：
![image](https://github.com/haodong-liu/-/blob/master/pic/7.png)
![image](https://github.com/haodong-liu/-/blob/master/pic/8.png)
![image](https://github.com/haodong-liu/-/blob/master/pic/9.png)

    这样我们可以得到一个商品所有特征值的TF_IDF，值越大，该特征对于该商品的重要程度越大。
    (其中所有的分母都+1，保证分母不为0)。
    计算出这些TF_IDF，在用余弦像是度来测算两个商品的相似程度，下面介绍一下余弦相似度算法，
    对于两个向量来说，之间的夹角越小，这两个向量靠的越近，针对我们的额题目，
    就是商品的特征向量之间，如果计算出来的夹角的余弦值越接近于1，
    那么这两个商品之间的相似度就越高。如果这两个商品不同类，
    那么存在以下可能，①两个商品是同一家店铺的不同类商品，属于同一个系列或者有着同一种描述，
    那就有可能是搭配的，如figure2所示。②有可能这两种商品不在同一家店中，
    但可能具有同种用途下互补的功能，比如沙滩裤，沙滩鞋，比基尼等商品都会有提到海边，
    沙滩，休闲这样的字眼，那这些商品之间就可能有搭配的潜在可能。 
    这里有一个问题，这个余弦值到底去多少，那才算是搭配的，这里经过对参数的控制，
    我们得出的余弦值在0.4~0.6之间，得出的结果还是可以的。具体的试验中，
    由于商品舒服过多，要基于30万件商品找到所有的搭配过于复杂，
    在计算TF_IDF是也要消耗大量时间，我们把数据集缩小，得出的结果也是比较令人欣慰的，
    所以我们大胆推测，当数据集变大时，这样的话，算出的结果就越好。
    针对这个模型，我们也给出了一个评价函数：
![image](https://github.com/haodong-liu/-/blob/master/pic/11.png)

    其中Vsim是候选商品的待预测商品之间的TF_IDF文本相似度，我们找到余弦相似度在0.4·0.6之间的商品，
    且S2较大的商品对，认为是搭配的。纳入搭配商品集合中。

### 3.相似商品达人搭配表中匹配
    这个模型的逻辑是这样的，在那么多的服装中，我们找到了与一件衣服A相似的商品B,C,D…
    而恰巧，这些B,C,D都在达人商品集合中出现过，存在与他们搭配的商品，
    那么巧了，这个衣服A是不是就能和与B,C,D搭配的商品搭配呢，答案是肯定的，
    如Figure 3所示。Figure3的思路是解释这个方法是否可行，我们做的时候，
    是反过来做的，我们先找与待测商品A相似的其他同类商品B,C,D….
    之后通过找B,C,D…在达人搭配表中的搭配商品，赋值给商品A的搭配商品（已经排除其他不可能的因素）。
    那我们这个模型就可以借助上一个模型计算商品间搭配程度的算法来找到，
    与之相似的其他商品，这样，我们借助这些商品的ID直接去【2】达人搭配套餐表中找这些商品的搭配商品，
    这样就能找到与待测商品相搭配的商品。
    这个模型所用到控制相似程度的余弦相似度我们控制在了0.75~1之间，
    因为这些都是找同类商品中相似商品，这样相似程度越高就是越相似的，
    不用考虑不同类之间的可能存在的商品描述有差异的问题。对于该问题，
    我们没有给出评价函数，是因为这些搭配的商品是从达人搭配表中直接获取的模式肯定搭配的，
    只可能是在找相似商品的时候，余弦相似度存在问题，
    那我们就按照余弦相似度排序就好了，越相似的商品的搭配商品，越搭配。

