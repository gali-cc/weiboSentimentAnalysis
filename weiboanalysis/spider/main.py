import os

from MySQLdb import ProgrammingError
from weiboanalysis.spider.article_spider import start as article_spider_start
from weiboanalysis.spider.comment_spider import start as comment_spider_start

from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine(
    "mysql+mysqldb://root:abc123@127.0.0.1:3306/db_weibo?charset=utf8mb4",
)

def dataClean():
    pass

def saveToDb():
    try:
        basePath = os.path.dirname(__file__)
        newArticle = pd.read_csv(os.path.join(basePath, 'article_data.csv'))
        newComment = pd.read_csv(os.path.join(basePath, 'comment_data.csv'))

        with engine.begin() as conn:
            # 先读取旧数据，再读取新数据
            oldArticle = pd.read_sql('SELECT * FROM t_article', con=conn)
            allArticle = pd.concat([oldArticle, newArticle], ignore_index=True)
            allArticle = allArticle.drop_duplicates(subset=['id'], keep='last')

            oldComment = pd.read_sql('SELECT * FROM t_comment', con=conn)
            allComment = pd.concat([oldComment, newComment], ignore_index=True)
            allComment = allComment.drop_duplicates(subset=['id'], keep='last')
           
            # 先删除旧数据，再插入新数据
            conn.execute(text("DELETE FROM t_article"))
            conn.execute(text("DELETE FROM t_comment"))
            allArticle.to_sql('t_article', con=conn, if_exists='append', index=False)
            allComment.to_sql('t_comment', con=conn, if_exists='append', index=False)

            os.remove(os.path.join(basePath, 'article_data.csv'))
            os.remove(os.path.join(basePath, 'comment_data.csv'))
    except Exception as e:
        print("数据持久化到数据库函数异常:", e)
        print("直接保存新数据")
        # 直接保存新数据
        with engine.begin() as conn:
            newArticle.to_sql('t_article', con=conn, if_exists='append', index=False)
            newComment.to_sql('t_comment', con=conn, if_exists='append', index=False)
        os.remove(os.path.join(basePath, 'article_data.csv'))
        os.remove(os.path.join(basePath, 'comment_data.csv'))
        

if __name__ == '__main__':
    print("==========微博文章内容爬取开始==========")
    article_spider_start()
    print("==========微博文章内容爬取完成==========")
    print("==========微博评论内容爬取开始==========")
    comment_spider_start()
    print("==========微博评论内容爬取完成==========")
    print("==========数据清洗开始==========")
    dataClean()
    print("==========数据清洗完成==========")
    print("==========数据持久化到数据库开始==========")
    saveToDb()
    print("==========数据持久化到数据库完成==========")
