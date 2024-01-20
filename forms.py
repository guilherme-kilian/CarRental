from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, RadioField, IntegerField, HiddenField, validators
from domain.customer import Customer
from domain.city import City

def customers():
    return [(r.id, r.name) for r in Customer.query.all()]

def cities():
    return [(r.id, r.name) for r in City.query.all()]

class AddCustomerForm(FlaskForm):
    name = StringField('Nome', validators=[validators.DataRequired()])
    submit = SubmitField('Criar')
    
class FilterRentalForm(FlaskForm):
    filter = SelectField('Filtro', coerce=int, choices=[(1, 'Nome do cliente'), (2, 'Modelo do veículo')])
    value = StringField('Valor', validators=[validators.DataRequired()])
    submit = SubmitField('Pesquisar')
    
class RentVehicleForm(FlaskForm):
    rented_days = IntegerField('Quantidade de diárias', validators=[validators.DataRequired()])
    vehicles = RadioField('Veículos', choices=[])
    customerId = HiddenField('CustomerId')
    originCityId = HiddenField('OriginCityId')
    submit = SubmitField('Alugar')
    
class ReturnVehicleForm(FlaskForm):
    customer_name = StringField('Nome do cliente', validators=[validators.DataRequired()])
    destine_city_id = SelectField('Cidade de destino', choices=cities, validators=[validators.DataRequired()])
    km_traveled = IntegerField('Kilometros viajados', validators=[validators.NumberRange(1)])
    return_vehicle = BooleanField('Confirmar devolução')
    submit = SubmitField('Devolver')    
        
class FilterVehicleForm(FlaskForm):
    filter = SelectField('Filtro', coerce=int, choices=[(1, 'Modelo'), (2, 'Cor'), (3, 'Ano'), (4, 'Cidade')])
    value = StringField('Valor', validators=[validators.DataRequired()])
    submit = SubmitField('Pesquisar')
    
class SearchVehicleForm(FlaskForm):
    customerId = SelectField('Cliente', choices=customers, validators=[validators.DataRequired()])
    originCityId = SelectField('Cidade de origem', choices=cities, validators=[validators.DataRequired()])
    submit = SubmitField('Pesquisar')