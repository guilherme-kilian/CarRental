from sqlalchemy import Column, Integer, String
from app import db

class Customer(db.Model):
    __tablename__ = 'customer'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(255))