from __future__ import annotations


from sqlalchemy import Integer, Column, String, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Route(Base):
    __tablename__ = "route"

    id = Column(Integer, primary_key=True, index=True)
    edges = Column(JSON, nullable=False)
    start = Column(String, nullable=False)
    end = Column(String, nullable=False)