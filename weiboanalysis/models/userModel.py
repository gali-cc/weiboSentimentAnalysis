from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from weiboanalysis.models import Base

class User(Base):
    __tablename__ = 't_user'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    createtime: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'<User {self.username}>'
 