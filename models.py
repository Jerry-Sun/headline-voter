from sqlalchemy import Column, Integer, String
from database import Base

class HeadlineScore(Base): 

    __tablename__ = "headline_scores"

    headline = Column(String, primary_key=True)
    score = Column(Integer)


