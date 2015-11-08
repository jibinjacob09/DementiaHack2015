from flask import Blueprint
from portal.common import app, db
from flask import render_template, abort, jsonify, request, make_response, json
import urllib
import urllib2
import uuid
import datetime

memory_api = Blueprint('memory_api', __name__)

@memory_api.route('/', methods=['GET'])
def getMemory(patientId):
	return "get memory api"
	
@memory_api.route('/', methods=['POST'])
def addMemory(patientId):
	return "add memory api"
	
	