from app import db
from models.filterType import FilterType
from models.filterVehicle import FilterVehicle
from models.statistics import Statistics
from domain.vehicle import Vehicle
from domain.city import City
from domain.customer import Customer
from domain.rental import Rental
from sqlalchemy import func
from models.resumeModel import *

class AppService():
    def __init__(self):
        super().__init__()        
        self.session = db.session    
        
    def init(self):        
        db.create_all()        
        db.session.commit()
        
    def get_vehicle_by_filter(self, filter, value):
        result = None        
        if filter is FilterType.City:
            city = self.session.query(City).where(City.name == value).first()
            result = self.session.query(Vehicle).where(Vehicle.city == city).all()
        elif filter is FilterType.Year:
            result = self.session.query(Vehicle).where(Vehicle.year == value).all()
        elif filter is FilterType.Color:
            result = self.session.query(Vehicle).where(Vehicle.color == value).all()
        elif filter is FilterType.Model:
            result = self.session.query(Vehicle).where(Vehicle.model == value).all()
        return result
    
    def get_rental_vehicle_by_filter(self, filter, value):
        result = None        
        if filter is FilterVehicle.ClientName:
            result = self.session.query(Rental).join(Vehicle).join(Customer).where(Customer.name == value).all()
        elif filter is FilterVehicle.VehicleModel:
            result = self.session.query(Rental).join(Vehicle).where(Vehicle.model == value).all()
            
        return result
        
    def get_vehicle_to_rent(self, customerId, originCityId):
        
        self.validate_active_rent(customerId)        
        vehicles = self.get_available_vehicles_by_city(originCityId)
        return vehicles
        
    def add_rental(self, customerId, vehicleId, originCityId, quantityDays):
        customer = self.get_customer(customerId)
        vehicle = self.get_vehicle(vehicleId)
        originCity = self.get_city(originCityId)
        
        vehicle.available = False
        rental = Rental(customer=customer, vehicle=vehicle, origin_city=originCity, rented_days=quantityDays, finished=False)
        self.add_and_save(rental)
        return rental
    
    def get_return_vehicle(self, customerName):
        rental = self.get_rental_by_customer_name(customerName)
        self.validate_notfound(rental, "Rental")
        return rental
        
    def return_vehicle(self, customerName, destineCityId, kilometer_traveled):
        rental = self.get_rental_by_customer_name(customerName)
        destineCity = self.get_city(destineCityId)
        
        rental.vehicle.odometer += kilometer_traveled
        rental.vehicle.available = True      
        rental.vehicle.city = destineCity
          
        rental.kilometer_traveled = kilometer_traveled
        rental.destine_city = destineCity
        rental.finished = True
        self.session.commit()        
        
        return rental

    def get_statistics(self):
        statistics = Statistics()
        statistics.totalDaysRented = self.session.query(func.sum(Rental.rented_days)).scalar()
        statistics.totalKmTraveled = self.session.query(func.sum(Rental.kilometer_traveled)).scalar()                
        statistics.totalKmTraveledValue = round(self.session.query(func.sum(Vehicle.kilometer_value * Rental.kilometer_traveled)).join(Rental, Vehicle.id == Rental.vehicle_id).scalar(), 2)
        statistics.totalDaysValue = round(self.session.query(func.sum(Vehicle.daily_value * Rental.rented_days)).join(Rental, Rental.vehicle_id == Vehicle.id).scalar(), 2)
        statistics.totalLocationValue = round(statistics.totalDaysValue + statistics.totalKmTraveledValue, 2)
        
        return statistics
        
    def get_rental_resume(self, customerName, kmTraveled):
        rent = self.get_rental_by_customer_name(customerName)        
        rented_days_value = rent.rented_days * rent.vehicle.daily_value
        km_traveled_value = round(kmTraveled * rent.vehicle.kilometer_value, 2)         
        return ResumeModel(rent.vehicle, rent.rented_days, rented_days_value, km_traveled_value, round(rented_days_value + km_traveled_value, 2))
    
    def validate_active_rent(self, customerId):
        rent = self.session.query(Rental).join(Customer).join(Vehicle).where(Customer.id == customerId).where(Rental.finished == False).first()
                
        if rent:
            raise Exception("RentNotFinishedPreviously")
        
    def get_rental_by_customer_name(self, customerName):
        rent = self.session.query(Rental).join(Customer).join(Vehicle).where(Customer.name == customerName).where(Rental.finished == False).first()
        self.validate_notfound(rent, "Rent")
        return rent
    
    def get_rental(self, id):
        return self.session.query(Rental).join(Vehicle).where(Rental.id == id).first()

    def get_customer_by_name(self, name):
        return self.session.query(Customer).where(Customer.name == name).first()
    
    def add_customer(self, name):
        
        customer = self.session.query(Customer).where(Customer.name == name).first()
        
        if customer is not None:
            raise Exception("CustomerAlreadyExists")
        
        newCustomer = Customer(name=name)
        self.add_and_save(newCustomer)
        return customer
    
    def get_customer(self, id):
        customer = self.session.query(Customer).where(Customer.id == id).first()
        self.validate_notfound(customer, "Customer")
        return customer
    
    def get_all_customers(self):
        return self.session.query(Customer).all()
    
    def get_all_cities(self):
        return self.session.query(City).all()
    
    def get_vehicle(self, id):
        vehicle = self.session.query(Vehicle).where(Vehicle.id == id).first()
        self.validate_notfound(vehicle, "Vehicle")
        return vehicle
    
    def get_available_vehicles_by_city(self, cityId):
        vehicle = self.session.query(Vehicle).where(Vehicle.city_id == cityId).where(Vehicle.available == True).all()
        self.validate_notfound(vehicle, "Vehicle")
        return vehicle
    
    def get_city(self, id):
        city = self.session.query(City).where(City.id == id).first()
        self.validate_notfound(city, "City")
        return city
    
    def add_and_save(self, obj):
        self.session.add(obj)
        self.session.commit()
    
    def validate_notfound(self, obj, objName):
        
        if isinstance(obj, list):                
            if(len(obj) == 0):
                raise Exception(objName + "_NotFound")
        else:
            if(obj is None):
                raise Exception(objName + "_NotFound")
        
        
        
        
        