from weiboanalysis.dao import articleDao
import jieba
import re
import pandas as pd


def save_word_fre_toCsv(sorted_word_fre_list, file_path='weiboanalysis/fenci/article_fre.csv'):
    """
    保存词频列表到文件，格式为 CSV 包含两列：热词、频率
    """
    df = pd.DataFrame(sorted_word_fre_list, columns=['热词', '频率'])
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    

def getStopwordList():
    """
    获取停顿词列表
    """
    with open('weiboanalysis/fenci/stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = f.readlines()
    stopwords = [word.strip() for word in stopwords]
    return stopwords

def cut_article():
    """
    对文章文本进行分词
    """
    articles = articleDao.getAllArticle() or []
    article_list = [article[1] for article in articles if len(article) > 1 and article[1]]
    all_articleStr = ''.join(article_list)
    seg_list = jieba.cut(all_articleStr)  # 默认是精确模式
    # print("精确模式: " + "/".join(seg_list))
    return seg_list


def word_fre_count():
    """
    统计分词结果中每个词的出现频率
    """
    seg_list = cut_article()
    stopWordList = getStopwordList()
    
    new_seg_list = []
    # 正则去掉数字， 单个字以及停顿词
    # 检测词中是否包含数字。如果 number is None ，说明这个词不含数字；再加上长度 > 1 且不在停用词表里，就保留到 new_seg_list 。
    for word in seg_list:
        number = re.search(r'\d+', word)
        if number is None and len(word) > 1 and word not in stopWordList:
            new_seg_list.append(word)
    
    # 统计词频
    word_fre = {}
    for word in new_seg_list:
        word_fre[word] = word_fre.get(word, 0) + 1

    # 按词频从高到低排序
    sorted_word_fre = sorted(word_fre.items(), key=lambda x: x[1], reverse=True)
    return sorted_word_fre



if __name__ == '__main__':
    # stopwords = getStopwordList()
    # print(stopwords)
    sorted_word_fre = word_fre_count()
    save_word_fre_toCsv(sorted_word_fre)
    pass
