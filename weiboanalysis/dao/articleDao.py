"""
文章数据访问对象
"""
from sqlalchemy import text

from weiboanalysis.extensions import engine


def getTotalArticleCount():
    """
    获取文章总数
    """
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("SELECT COUNT(*) FROM t_article"))
            return rows.fetchone()[0]
    except Exception as e:
        print("获取文章总数函数异常:", e)
        return None

def getTopAuthor():
    """
    获取点赞最高的作者
    """
    try:
        with engine.connect() as conn:
            rows = conn.execute(text("SELECT authorName FROM t_article ORDER BY attitudes_count DESC LIMIT 0, 1"))
            return rows.fetchone()[0]
    except Exception as e:
        print("获取点赞最高的作者函数异常:", e)
        return None

def getTopRegion():
    """
    获取点赞最高的城市
    """
    try:
        with engine.connect() as conn:
            stmt = "SELECT region_name, SUM(attitudes_count) AS ac FROM t_article WHERE region_name IS NOT NULL " \
                    "GROUP BY region_name ORDER BY ac DESC LIMIT 0, 1"
            rows = conn.execute(text(stmt))
            return rows.fetchone()[0]
    except Exception as e:
        print("获取点赞最高的城市函数异常:", e)
        return None

def getArticleTopZan():
    """
    获取点赞最高的6条帖子
    """
    try:
        with engine.connect() as conn:
            stmt = "SELECT text_raw, attitudes_count FROM t_article ORDER BY attitudes_count DESC LIMIT 0, 6"
            rows = conn.execute(text(stmt))
            return [list(row) for row in rows.fetchall()]
    except Exception as e:
        print("获取点赞最高的文章函数异常:", e)
        return None

def get7DayArticleCount():
    """
    获取最近7天内的文章总数
    """
    try:
        with engine.connect() as conn:
            stmt = "SELECT DATE_FORMAT(created_at, '%Y-%m-%d') AS articleDate, COUNT(text_raw) AS articleTotal FROM t_article "\
                "GROUP BY articleDate ORDER BY articleDate DESC LIMIT 0, 7"
            rows = conn.execute(text(stmt))
            return [list(row) for row in rows.fetchall()]
    except Exception as e:
        print("获取最近7天内的文章总数函数异常:", e)
        return None
    
def getArticleTypeAmount():
    """
    获取文章类型数量
    """
    try:
        with engine.connect() as conn:
            stmt = "SELECT articleType, COUNT(articleType) as ac FROM t_article GROUP BY articleType"
            rows = conn.execute(text(stmt))
            return [list(row) for row in rows.fetchall()]
    except Exception as e:
        print("获取文章类型数量函数异常:", e)
        return None

def getAllArticle():
    """
    获取所有文章
    """
    try:
        with engine.connect() as conn:
            stmt = "SELECT * FROM t_article"
            rows = conn.execute(text(stmt))
            return [list(row) for row in rows.fetchall()]
    except Exception as e:
        print("获取所有文章函数异常:", e)
        return None

def getArticleByArcType(articleType: str):
    """
    根据文章类型获取文章
    """
    try:
        with engine.connect() as conn:
            stmt = "SELECT * FROM t_article WHERE articleType = :articleType"
            rows = conn.execute(text(stmt), {'articleType': articleType})
            return [row for row in rows.fetchall()]
    except Exception as e:
        print("根据文章类型获取文章函数异常:", e)
        return None


def getArticleIPData():
    """
    获取文章IP数据
    """
    try:
        with engine.connect() as conn:
            stmt = """
                SELECT region_name, COUNT(region_name) AS ac FROM t_article WHERE region_name IS NOT NULL 
                GROUP BY region_name ORDER BY ac DESC
            """
            rows = conn.execute(text(stmt))
            return [list(row) for row in rows.fetchall()]
    except Exception as e:
        print("获取文章IP数据函数异常:", e)
        return None