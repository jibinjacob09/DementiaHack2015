from flask import Blueprint
from portal.common import app, db
from flask import render_template, abort, jsonify, request, make_response, json
import urllib
import urllib2

caretaker_api = Blueprint('caretaker_api', __name__)

@caretaker_api.route('/', methods=['POST'])

#Function to create Caregiver to database  (called by Portal)
def createCareGiver():
    #preconditions:  table exists -> Caregiver ID, Date joined, Name, email

    	#Info of Caregiver (NOT WORKING ATM)
    	caregiver_name = 'Fry Phil'
    	caregiver_email = 'Fry@planetexpress.uni'

    	#creating the cursor
    	cur = db.cursor()

    	try: #attempt to create a new caregiver profile
    		cur.execute("INSERT INTO care_giver(date_created, name, email) VALUES (NOW(), 'Fry Phil', 'Fry@planetexpress.uni')")
    	except Exception, e:
    		return "Error creating care_giver"   #if something went wrong with adding to the table

    	cur.close()
    	db.commit()

    #postconditions:  successfuly inserted -> generate a confirmation token
    	return "successfull"  #indicating everything was good

#    return render_template('elections.html')
