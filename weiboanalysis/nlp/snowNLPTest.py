from snownlp import SnowNLP
pos_text = "这家餐厅环境优雅，菜品新鲜！"
neg_text = "服务差，价格贵，再也不来了。"
pos_score = SnowNLP(pos_text).sentiments  # ≈0.99
neg_score = SnowNLP(neg_text).sentiments  # ≈0.01
print(pos_score, neg_score)