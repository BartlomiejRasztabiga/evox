from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(length=160), nullable=False)
    views_count = Column(Integer, nullable=False, default=0)
