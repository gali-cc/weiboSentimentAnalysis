import os
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

def genWordCloudPic(str, maskImg, outImg):
    """
    genWordCloudPic 的 Docstring
    生成词云图片

    :param str: 输入的词云文本 空格分隔
    :param maskImg: 词云形状图片路径
    :param outImg: 输出的词云图片路径
    """
    img = Image.open(maskImg)
    img_arr = np.array(img) # 将图片转换为数组    
    wc = WordCloud(
            font_path='weiboanalysis/wordcloud/STHUPO.TTF', # 字体文件路径
            background_color='white', # 背景颜色
            colormap='viridis', # 颜色映射
            width=800, # 宽度
            height=600, # 高度
            mask=img_arr, # 词云形状, 这里使用文章图片作为词云形状
        )
    wc.generate_from_text(str) # 从文本生成词云
    
    # 显示词云
    # interpolation='bilinear' 插值方法, 这里使用双线性插值
    plt.imshow(wc, interpolation='bilinear')
    # 隐藏坐标轴
    plt.axis('off')
    # 保存词云图片
    plt.savefig(outImg, dpi=500) # 保存词云图片, dpi=500 分辨率为500


if __name__ == '__main__':
    text = "牛掰 牛逼 大佬 我去 张三 卡卡 嘿嘿 哈哈 生成 商城 气死我了 不去 就不要 好滴 \
        骄傲 好的 大战 发展 求生 共存 火了 刘安 伙计 火鸡 打火机"
    # 生成词云
    basePath = os.path.dirname(__file__)
    maskImg = os.path.join(basePath, 'comment_mask.jpg') 
    outImg = os.path.join(basePath, 'wordcloud2.png')

    genWordCloudPic(text, maskImg, outImg)

 