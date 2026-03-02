import os
from wordcloud import WordCloud
from PIL import Image
import numpy as np

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
            width=1600, # 宽度
            height=1200, # 高度
            mask=img_arr, # 词云形状, 这里使用文章图片作为词云形状
            scale=2, # 缩放比例
            prefer_horizontal=0.9, # 水平方向的字体比例
        )
    wc.generate_from_text(str) # 从文本生成词云
    output_path = os.path.join('weiboanalysis', 'static', outImg)
    wc.to_file(output_path)
