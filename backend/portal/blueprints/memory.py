from flask import Blueprint
from portal.common import app, db
from portal.util import createErrorResponse
from flask import render_template, abort, jsonify, request, make_response, json
import urllib
import urllib2
import uuid
import datetime

memory_api = Blueprint('memory_api', __name__)

@memory_api.route('/<int:patientId>', methods=['GET'])
def getMemory(patientId):
	#make sure to include ?search=something when using this
	cur = db.cursor()
	try:
		searchkeys = request.args.getlist("searchkeys")
		
		# search for all rows in recall_db where patientid = patientid and (word = searchkeys[i] OR word = searchkey[i+1])
		format_strings = ','.join(['%s'] * len(searchkeys))		
		cur.execute("select distinct passage from keys_db left join memory using(memory_id) where patient_id = %s and word IN ({0}) order by date_created desc".format(format_strings), (patientId, tuple(searchkeys)))
		rows = cur.fetchall()
		
		memory_list = []
		for row in rows:
			memory_list.append(row[0])
	except Exception, e:
		return createErrorResponse("Problem in the Get function of memory.py", e, 500)

	cur.close()
	db.commit()
	return jsonify({'memories': memory_list})

@memory_api.route('/<int:patientId>', methods=['POST'])
def addMemory(patientId):
	cur = db.cursor()
	
	# sample input
	# {
	#	"keywords": [
	#		"a",
	#		"b"
	#	],
	#	"message": "keys on fridge!"
	# }
	
	data = request.data
	dataDirt = json.loads(data)

	#follow the JSON I gave out!
	message = dataDirt['message']

	try:
		#insert memory into memory table
		cur.execute("INSERT INTO memory (patient_id, date_created, passage) VALUES (%s, NOW(), %s)", (patientId, message))
		memory_last_id = cur.lastrowid
		for key in dataDirt['keywords']:
			print(key)
			#insert key words into keyword table
			cur.execute("INSERT INTO keys_db (memory_id, word) VALUES (%s, %s)", (memory_last_id, key))
			key_last_id = cur.lastrowid
			cur.execute("SELECT * FROM recall_db WHERE word = %s AND patient_id = %s", (key, patientId))
			data = cur.fetchall()
			#if this is the first entry
			if len(data) == 0:
				cur.execute("INSERT INTO recall_db (word, memory_id, patient_id, search_count, store_count) VALUES (%s, %s, %s, %s, %s)", (key, memory_last_id, patientId, 0, 1))
				print("creating first entry")
			#If an entry is already there
			else:
				cur.execute("SELECT store_count FROM recall_db WHERE word = %s AND patient_id = %s", (key, patientId))
				data = cur.fetchall()
				count = 0
				#iterate the counter
				for row in data:
					 count = str(row[0])
				new_count = int(count) + 1
				cur.execute("UPDATE recall_db SET store_count = %s WHERE patient_id = %s AND word = %s", (new_count, patientId, key))
	#Error!
	except Exception, e:
		return createErrorResponse("Something went wrong in post of memory.py", e, 500)
	cur.close()
	db.commit()
	return jsonify({'errors': False})
