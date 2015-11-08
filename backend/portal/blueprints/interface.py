from flask import Blueprint
from portal.common import app, db
from flask import render_template, abort, jsonify, request, make_response, json
import urllib
import urllib2

interface_api = Blueprint('interface_api', __name__)

@interface_api.route('/')
@interface_api.route('/index')
def index():
    return render_template('index.html')
