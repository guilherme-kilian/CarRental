from sqlalchemy import Column, Integer, String
from app import db

class City(db.Model):
    __tablename__ = 'city'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(255))