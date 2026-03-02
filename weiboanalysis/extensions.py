from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqldb://root:abc123@127.0.0.1:3306/db_weibo?charset=utf8mb4",
    pool_pre_ping=True,
    pool_recycle=3600,
)
