import os
from flask import Flask
import MySQLdb

app = Flask(__name__, static_url_path='', instance_relative_config=True)

app.config.from_object('config')
config_name = os.getenv('FLASK_CONFIG', 'default')
if config_name == 'dev':
    app.config.from_pyfile('config.py')

db = None
try:
    db = MySQLdb.connect(host=app.config['MYSQL_HOST'],
                        user=app.config['MYSQL_USER'], 
                        passwd=app.config['MYSQL_PASSWORD'],
                        db=app.config['MYSQL_DB'])
except:
    print "Could not connect to database at " + app.config['MYSQL_HOST']
    
    
from blueprints import patient_blueprint, caretaker_blueprint, interface_blueprint, memory_blueprint
app.register_blueprint(patient_blueprint, url_prefix='/api/patient')
app.register_blueprint(caretaker_blueprint, url_prefix='/api/caretaker')
app.register_blueprint(memory_blueprint, url_prefix='/api/memory')
app.register_blueprint(interface_blueprint, url_prefix='')