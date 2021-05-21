from sqlalchemy import Column, Integer

from app.db.base_class import Base


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
