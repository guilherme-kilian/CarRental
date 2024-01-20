from sqlalchemy import Column, Integer, Boolean, Float, String, ForeignKey
from app import db
import sqlalchemy.orm as orm
from domain.city import City

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    __table_args__ = { 'extend_existing': True }
    id = Column(Integer, primary_key=True)       
    city_id = Column(Integer, ForeignKey(City.id), nullable=False)     
    city = orm.relationship(City, backref='city', foreign_keys=[city_id])
    model = Column(String(255))
    color = Column(String(255))
    year = Column(Integer)
    odometer = Column(Integer)
    available = Column(Boolean)
    daily_value = Column(Float)
    kilometer_value = Column(Float)