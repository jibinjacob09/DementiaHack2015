from flask import Blueprint
from portal.common import app, db
from flask import render_template, abort, jsonify, request, make_response, json
import urllib
import urllib2
import datetime

caretaker_api = Blueprint('caretaker_api', __name__)

@caretaker_api.route('/', methods=['POST'])

#Function to create Caregiver to database  (called by Portal)
def createCareGiver():
    #preconditions:  table exists -> Name, email

        #getting name and email from Portal
            #sample input argument
                #{
                #    "name" : "zioberg",
                #    "email" : "crabby@baddoctors.mu"
                #}
        try:
       	    data = request.data
       	    dataDirt = json.loads(data);
        except Exception, e:
            return "ERROR, need name & email"

        caregiver_name = dataDirt['name']
        caregiver_email = dataDirt['email']

    	#creating the cursor
    	cur = db.cursor()

    	try: #attempt to create a new caregiver profile
    		cur.execute("INSERT INTO care_giver(date_created, name, email) VALUES (NOW(), %s, %s)", (caregiver_name, caregiver_email))
    	except Exception, e:
    		return "Error creating care_giver"   #if something went wrong with adding to the table

        stored_id = cur.lastrowid
    	cur.close()
    	db.commit()

    #postconditions: if success then return Caregiver ID
    	return jsonify({'caretakerID':stored_id}) #indicating everything was good

@caretaker_api.route('/<int:caretakerId>/<int:patientId>/', methods=['GET'])
#Function to Pair caregiver and patients (called by Portal)
def patient_cg(caretakerId,patientId):
    #preconditions table exists -> patient Id, caregiver id

    cur = db.cursor()

    try: #attempting to combine the patient and the caregiver and timestamp
        cur.execute("INSERT INTO patient_cg (care_giver_id, patient_id, time_created) VALUES (%s, %s, NOW())", (caretakerId, patientId))
    except Exception, e:
        return "Error combining"  #if something goes wrong

    cur.close()
    db.commit()

    # postconditions: if sucess -> generate a confirmation token
    return jsonify({"success":1})

@caretaker_api.route('/<int:caretakerId>/patients/', methods=['GET'])
#Function to Return Patient List (called by Portal)
def PatientList(caretakerId):
    #preconditions: need Caregiver ID
    cur = db.cursor()

    try: #attempting to info of all patient for a particualr caretaker
        cur.execute("SELECT patient_id FROM patient_cg WHERE care_giver_id = %s", caretakerId)
        data = cur.fetchall()
    except Exception, e:
        return "Error looking"  #if something goes wrong

    cur.close()

    tmp_str = ""

    for row in data  :  #concatente all patient ids into one string
        tmp_str = tmp_str + str(row[0])
        tmp_str = tmp_str + ","
#postconditions: returns a string with all the patient connected to caregiver
    return (tmp_str)
