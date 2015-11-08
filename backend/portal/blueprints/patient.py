from flask import Blueprint
from portal.common import app, db
from flask import render_template, abort, jsonify, request, make_response, json
import urllib
import urllib2
import uuid
import datetime


patient_api = Blueprint('patient_api', __name__)

@patient_api.route('/', methods=['POST'])

#creating a patient row into the database

def createPatient(): #function to create (or add) new patients

	#Info of patient (NOT WORKING ATM)
	patient_name = 'Fry Phil'
	patient_email = 'Fry@planetexpress.uni'

	#creating the cursor
	cur = db.cursor()

	try: #attempt to create a new patient profile
		cur.execute("INSERT INTO patient(date_created, name, email) VALUES (NOW(), 'Bender', 'bender@momsrobot.ui')")
	except Exception, e:
		return "error creating patient"   #something went wrong with adding to the table

	cur.close()
	db.commit()

	return "created patient api"  #indicating everything was good

#@patient_api.route('/<int:patientId>/mostsearched/', methods=['POST'])


#def mostsearched(patientId): #function to

#	Id = patientId
#	cur = db.cursor()

#	try:
#		cur.execute("INSERT INTO storing(patient_id, keyword, count, date_stamp) VALUES (Id, 'word', 1, NOw())")
#	return "inprogress"


@patient_api.route('/<int:patientId>', methods=['GET'])
def getPatient(patientId):
	return "get patient " + str(patientId)
