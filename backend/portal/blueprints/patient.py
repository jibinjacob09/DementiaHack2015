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

#Function to add Patient to the database  (call by app)
def createPatient():
	#requirements: table exists -> name (optional), email (optional)

 	#getting name and email from app
		#sample input argument
			#{
    		#	"name" : "leela",
    		#	"email" : "oneeyed@purplehair.org"
			#}

	data = request.data
	dataDirt = json.loads(data)

	patient_name = dataDirt['name']
	patient_email = dataDirt['email']


	#creating the cursor
	cur = db.cursor()

	try: #attempt to create a new patient profile
		cur.execute("INSERT INTO patient(date_created, name, email) VALUES (NOW(), %s, %s)", (patient_name, patient_email))
	except Exception, e:
		return "error creating patient"   #something went wrong with adding to the table

	db.commit()
	stored_id = cur.lastrowid
	cur.close()

	#postconditions:  if adding is scucessfull -> return Patient ID to app
	return jsonify({'patientId': stored_id})
@patient_api.route('/<int:patientId>/', methods=['GET'])
#Function to Return a single Patient login information (called by Portal)
def Patientinfo( patientId):
    #preconditions: patientId from portal
    cur = db.cursor()

    try:
        cur.execute("SELECT date_created, name, email FROM patient WHERE patient_id = %s", patientId)
        data = cur.fetchone()
    except Exception, e:
        return "Error looking Patientinfo"  #if something goes wrong

	cur.close()
    return jsonify({"output" : data } )
    #aim => postconditions: patient name, email, datejoined

@patient_api.route('/<int:patientId>/memories/', methods=['GET'])
#Function to Return all memories of one patient (called by Portal)
#preconditions: need Patient ID
def PatientMemories(patientId):
    cur = db.cursor()

    try:
        cur.execute("SELECT date_created, passage FROM memory WHERE patient_id = %s", patientId)
        data = cur.fetchall()
    except Exception, e:
        return "Error retriving memories"

    tmp_str = ""
    for row in data :   #concatenting all the memories to one string
        tmp_str = tmp_str + str(row)
        tmp_str = tmp_str + '\n'  #line break to sep memories

    cur.close()
#postconditions: returns one string with all the memories
    return (tmp_str)

@patient_api.route('/<int:patientId>/moststored/', methods=['GET'])
#function to call Most_Stored (called by Portal)
    #preconditions patientID
def PatientMostStored(patientId):
	cur = db.cursor()
	# 	print(patientId)
	temp = ""
	try:
	######  NEEDS TO BE FIXED !!!!!!!
		cur.execute("SELECT word,MAX(store_count) FROM recall_db where patient_id = %s", (patientId))
	except Exception,e :
		return "Error finding most stored"

	row = cur.fetchone()
	cur.close()
	#return "stored"
	return jsonify({"Most_Stored" : row})


@patient_api.route('/<int:patientId>/mostsearched/', methods=['GET'])
#function to call Most_Stored (called by Portal)
    #preconditions patientID
def PatientMostSearched(patientId):
	cur = db.cursor()
	# 	print(patientId)
	temp = ""
	try:
		cur.execute("SELECT word,MAX(search_count) FROM recall_db where patient_id = %s", (patientId))
	except Exception,e :
		return "Error finding most stored"

	row = cur.fetchone()
	cur.close()
	#return "stored"
	return jsonify({"Most_Searched" : row})
