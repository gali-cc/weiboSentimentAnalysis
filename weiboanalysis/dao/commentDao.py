from sqlalchemy import text

from weiboanalysis.extensions import engine


def getAllComment():
    try:
        with engine.begin() as conn:
            rows = conn.execute(text("SELECT * FROM t_comment WHERE text_raw != ''"))
            return rows.fetchall()
    except Exception as e:
        print("获取所有评论信息函数异常:", e)
        return None

def getTopCommentUsers():
    """
    获取Top评论数量前50的用户
    """
    try:
        with engine.connect() as conn:
            stmt = "SELECT userName, COUNT(userName) AS unCount FROM t_comment GROUP BY userName ORDER BY unCount DESC LIMIT 0, 50"
            rows = conn.execute(text(stmt))
            return [row[0] for row in rows.fetchall()]
    except Exception as e:
        print("获取评论最高的用户函数异常:", e)
        return None


def getCommentAmount():
    """
    获取最近7天评论总数
    """
    try:
        with engine.connect() as conn:
            stmt = "SELECT DATE_FORMAT(created_at, '%Y-%m-%d') AS commentDate, COUNT(text_raw) AS commentTotal FROM t_comment" \
                " GROUP BY commentDate ORDER BY commentDate DESC LIMIT 0, 7"
            rows = conn.execute(text(stmt))
            return [row for row in rows.fetchall()]
    except Exception as e:
        print("获取评论总数函数异常:", e)
        return None

def getCommentHotWordAmount(hotWord: str):
    """
    获取日期用户评论中热词数量
    """
    try:
        with engine.connect() as conn:
            # 1. 使用 :variable 占位符，而不是 f-string
            stmt = text("""
                SELECT DATE_FORMAT(created_at,'%Y-%m-%d') AS commentDate, 
                       COUNT(text_raw) AS commentTotal 
                FROM t_comment 
                WHERE LOCATE(:word, text_raw) > 0 
                GROUP BY commentDate 
                ORDER BY commentDate DESC
            """)
            
            # 2. 在 execute 时通过字典传入参数
            # SQLAlchemy 会自动处理 hotWord 里的特殊字符，使其失效
            rows = conn.execute(stmt, {"word": hotWord})
            return [row for row in rows.fetchall()]
    except Exception as e:
        print("获取评论中热词数量函数异常:", e)
        return None

def getCommentByHotWord(hotWord: str):
    """
    根据热词获取评论信息
    """
    try:
        with engine.connect() as conn:
            # 1. 使用 :variable 占位符，而不是 f-string
            stmt = text("""
                SELECT * FROM t_comment 
                WHERE LOCATE(:word, text_raw) > 0 
            """)
            
            # 2. 在 execute 时通过字典传入参数
            # SQLAlchemy 会自动处理 hotWord 里的特殊字符，使其失效
            rows = conn.execute(stmt, {"word": hotWord})
            return [row for row in rows.fetchall()]
    except Exception as e:
        print("获取评论中包含热词的评论函数异常:", e)
        return None

def getCommentIPData():
    """
    获取评论IP数据
    """
    try:
        with engine.connect() as conn:
            stmt = """
                SELECT source, COUNT(source) AS ac FROM t_comment WHERE source IS NOT NULL 
                GROUP BY source ORDER BY ac DESC
            """
            rows = conn.execute(text(stmt))
            return [list(row) for row in rows.fetchall()]
    except Exception as e:
        print("获取评论IP数据函数异常:", e)
        return None

if __name__ == '__main__':
    # getAllComment()
    pass
