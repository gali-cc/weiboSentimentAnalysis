import jieba
text = "自然语言处理是人工智能领域的重要方向"
seg_list = jieba.cut(text)
print("精确模式: " + "/".join(seg_list))
seg_list_full = jieba.cut(text, cut_all=True)
print("全模式: " + "/".join(seg_list_full))
seg_list_search = jieba.cut_for_search(text)
print("搜索引擎模式: " + "/".join(seg_list_search))
