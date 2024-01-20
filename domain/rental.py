from sqlalchemy import Column, Integer, ForeignKey, Boolean
from app import db
import sqlalchemy.orm as orm
from domain.customer import Customer
from domain.vehicle import Vehicle
from domain.vehicle import City

class Rental(db.Model):
    __tablename__ = 'rental'
    __table_args__ = { 'extend_existing': True }
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey(Customer.id, ondelete="CASCADE"), nullable=False)
    customer = orm.relationship(Customer, backref='customer', foreign_keys=[customer_id])
    vehicle_id = Column(Integer, ForeignKey(Vehicle.id), nullable=False)
    vehicle = orm.relationship(Vehicle, backref='vehicle', foreign_keys=[vehicle_id])
    origin_city_id = Column(Integer, ForeignKey(City.id), nullable=False)
    origin_city = orm.relationship(City, backref='origin_city', foreign_keys=[origin_city_id])
    destine_city_id = Column(Integer, ForeignKey(City.id))
    destine_city = orm.relationship(City, backref='destine_city', foreign_keys=[destine_city_id])    
    kilometer_traveled = Column(Integer)
    rented_days = Column(Integer)
    finished = Column(Boolean, nullable=False)