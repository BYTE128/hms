from flask import Flask
from config import Config
from mysql.connector import connect

app = Flask(__name__)
app.config.from_object(Config)

myDb = connect(host="localhost", port="3308", user="root", password="", database="hms")

from application.manageDiagnostics import manageDiagnostics
from application.managePatientInformation import managePatientInformation
from application.managePharmacyDetails import managePharmacyDetails
from application.onlineSearch import onlineSearch
from application.patientBilling import patientBilling
from application.websiteLogin import websiteLogin
from application import main

app.register_blueprint(manageDiagnostics.bp, url_prefix = '/manageDiagnostics')
app.register_blueprint(managePatientInformation.bp, url_prefix = '/managePatientInformation')
app.register_blueprint(managePharmacyDetails.bp, url_prefix = '/managePharmacyDetails')
app.register_blueprint(onlineSearch.bp, url_prefix = '/onlineSearch')
app.register_blueprint(patientBilling.bp, url_prefix = '/patientBilling')
app.register_blueprint(websiteLogin.bp, url_prefix = '/websiteLogin')
app.register_blueprint(main.bp)
