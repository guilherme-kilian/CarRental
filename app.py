from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:XFT4om48%zCVTc@localhost:3306/carRental'
app.config['SECRET_KEY'] = 'batatinha123'
db = SQLAlchemy(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True)