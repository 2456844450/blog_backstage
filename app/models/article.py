



from app.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean
class Article(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    desc = Column(String(100), nullable=False)
    author = Column(String(20))
    img_url = Column(String(100))
    comments = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    views = Column(Integer, default=0)
    state = Column(Integer, default=1)
    year = Column(Integer, default=0)

    field = Column(Integer, default=0)

    project_name = Column(String(100))
    project_url = Column(String(100))
    start_time = Column(String(100))
    end_time = Column(String(100))

    numbers = Column(Integer, default=0)

    tags = Column(String(100))

    content = Column(String(10000))

    keyword = Column(String(50))