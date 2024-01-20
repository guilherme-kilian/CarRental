from app import app
from flask import render_template, request, make_response, redirect, url_for
from appservice import *
from forms import *
from models.keyValueType import *
import json
from datetime import datetime as dt
import html2text
import os

appService = AppService()
folderPath = './reports/'

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    appService.init()
    return render_template('index.html')

@app.route('/customer', methods=['GET','POST'])
def customer():    
    form = AddCustomerForm()

    try:
        if form.validate_on_submit():
            customer = appService.add_customer(name=form.name.data)
            return render_template('customer.html', form=form, success=True, successMessage="Usuário criado com sucesso!")
    except Exception as ex:
        errorMessage = 'Erro interno'
        if str(ex) == 'CustomerAlreadyExists':
            errorMessage = 'Já existe um usuário criado com este nome'
            return render_template('customer.html', form=form, error=True, errorMessage=errorMessage)
        
    return render_template('customer.html', form=form)

@app.route('/vehicles', methods=['GET','POST'])
def vehicles():
    form = FilterVehicleForm()
    
    if form.validate_on_submit():
        vehicles = appService.get_vehicle_by_filter(filter=form.filter.data, value=form.value.data)
        return render_template('vehicles.html', form=form, vehicles=vehicles)
        
    return render_template('vehicles.html', form=form)

@app.route('/vehicles/rent', methods=['GET', 'POST'])
def vehicles_rent():
    form = SearchVehicleForm()        
    try:
        if form.validate_on_submit():
            formRent = RentVehicleForm()        
            populateChoices(formRent, form.customerId.data, form.originCityId.data)        
            formRent.customerId.default = form.customerId.data
            formRent.originCityId.default = form.originCityId.data
            return render_template('rent-car.html', form=form, formRent=formRent)          
    except Exception as ex:
        errorMessage = 'Erro interno.'
        if str(ex) == 'RentNotFinishedPreviously':
            errorMessage = 'Este cliente já possui uma locação em andamento.'
        
        if str(ex) == 'Vehicle_NotFound':
            errorMessage = 'Não há veículos disponíveis na cidade selecionado'
            
        return render_template('rent-car.html', form=form, error=True, errorMessage=errorMessage)
    
    return render_template('rent-car.html', form=form, error=False)

@app.route('/vehicles/rent/add', methods=['GET', 'POST'])
def vehicles_rent_add():   
    formSearch = SearchVehicleForm()  
    form = RentVehicleForm()      
    populateChoices(form, form.customerId.data, form.originCityId.data)    
    
    if form.validate_on_submit():
        appService.add_rental(customerId=form.customerId.data, vehicleId=form.vehicles.data, originCityId=form.originCityId.data, quantityDays=form.rented_days.data)
        return render_template('rent-car.html', success=True, successMessage="Locação realizada com sucesso!", form=formSearch)
    
    return render_template('rent-car.html', form=formSearch, formRent=form)

def populateChoices(formRent, customerId, cityId):
    vehicles = appService.get_vehicle_to_rent(customerId, cityId)
    data = lambda: [(v.id, v.model) for v in vehicles]
    formRent.vehicles.choices = data()

@app.route('/vehicles/return', methods=['GET', 'POST'])
def vehicles_return():
    
    form = ReturnVehicleForm()
    
    try:        
        if form.validate_on_submit():        
            if form.return_vehicle.data:
                appService.return_vehicle(form.customer_name.data, form.destine_city_id.data, form.km_traveled.data)
                return render_template('return-car.html', form=form, success=True, successMessage="Devolução realizada com sucesso!")
                            
            resume = appService.get_rental_resume(form.customer_name.data, form.km_traveled.data)
            
            return render_template('return-car.html', form=form, resume=resume, showResume=True)
    except Exception as ex:
        errorMessage = 'Erro interno.'        
        if str(ex) == 'Rent_NotFound':
            errorMessage = "Locação não encontrada"
        return render_template('return-car.html', form=form, error=True, showResume=False, errorMessage=errorMessage)
            
    return render_template('return-car.html', form=form, error=False, showResume=False)

@app.route('/statistics', methods=['GET'])
def resume():    
    statistics = appService.get_statistics()
    return render_template('statistics.html', statistics=statistics)

@app.route('/vehicles/<id>', methods=['GET', 'POST'])
def vehicle_by_id(id):
    vehicle = appService.get_vehicle(id)    
    return make_response(json.dumps({ 'color': vehicle.color, 'model': vehicle.model, 'year': vehicle.year }), 200, default_headers())

@app.route('/rentals', methods=['GET', 'POST'])
def rentals():        
    form = FilterRentalForm()       
    
    if form.validate_on_submit():
        rentals = appService.get_rental_vehicle_by_filter(filter=form.filter.data, value=form.value.data)        
        canDownload = rentals is not None        
        return render_template('rentals.html', form=form, rentals=rentals, canDownload=canDownload)
    
    return render_template('rentals.html', form=form, canDownload=False)

@app.route('/rentals/download', methods=['POST'])

def download():
        
    body = request.data.decode('utf-8')
    content = html2text.html2text(body)
    
    os.makedirs(folderPath, exist_ok=True)
    
    fileName = 'report-' + dt.now().strftime('%Y-%m-%d-%H-%M-%S') + '.md'
        
    with open(folderPath + fileName, 'w') as file:
        file.write(content)  
        
    return make_response({ "fileUrl": f'/rentals/download/{fileName}'})

@app.route('/rentals/download/<fileName>', methods=['GET'])
def reports(fileName):        
    with open(folderPath + fileName, 'r') as file:
        content = file.read()
        response = make_response(content)
        response.headers.set('Content-Type', 'text')
        response.headers.set('Content-Disposition', 'attachment', filename='report.txt')
        return response

def list_key_value(obj):
    return list(map(to_key_value_type, obj))

def to_key_value_type(obj):
    return KeyValueType(key=obj.id, value=obj.name)

def default_headers():
    return {"Content-Type": "application/json"}