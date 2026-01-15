from sqlalchemy import Column, Integer, String, Float
from db import Base

class Chemical(Base):
    __tablename__ = "chemicals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    formula = Column(String, nullable=True)
    quantity = Column(Float, default=0.0)
    location = Column(String, nullable=True)
    hazard = Column(String, nullable=True)
