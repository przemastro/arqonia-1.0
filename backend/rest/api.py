from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory
from flask_restful import reqparse, Api, Resource, abort
from JsonBuilder import json_data, json_load, json_diagram, json_hrdiagram
from JsonParser import json_parser, updateObservation, addUser, verifyCredentials
from ProcRunner import procRunner, deleteObservation
import os
import ConfigParser
import threading
import time
import logging
import random
from threading import *
import multiprocessing, time, signal
from flask_mail import Mail, Message





app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'HRHomeSurvey@gmail.com'
app.config['MAIL_PASSWORD'] = 'astroApp1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail()
mail.init_app(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'
api = Api(app)



config = ConfigParser.RawConfigParser()
config.read('../resources/ConfigFile.properties')
serverAddress = config.get('Server', 'server.address');

json_data()
json_load()
json_diagram()
json_hrdiagram()

Observations = json_data.jsonData
LastLoad = json_load.jsonLastLoad
ObservationsDiagram = json_diagram.jsonDiagram
ObservationsHRDiagram = json_hrdiagram.jsonHRDiagram

REST = {'observations': Observations,
        'lastLoad': LastLoad,
        'observationsDiagram': ObservationsDiagram,
        'observationsHRDiagram': ObservationsHRDiagram
        }


def abort_if_json_doesnt_exist(rest_id):
    if rest_id not in REST:
        abort(404, message="Deeply sorry but Json {} doesn't exist".format(rest_id))


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('startDate', type=str)
parser.add_argument('endDate', type=str)
parser.add_argument('uName', type=str)
parser.add_argument('uFileName', type=str)
parser.add_argument('vName', type=str)
parser.add_argument('vFileName', type=str)
parser.add_argument('bName', type=str)
parser.add_argument('bFileName', type=str)
parser.add_argument('id', type=str)
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)



class Rest(Resource):
    def get(self, rest_id):
            abort_if_json_doesnt_exist(rest_id)
            return REST[rest_id]


class RestObservation(Resource):
    def post(self):
            args = parser.parse_args()
            json_parser(args['name'], args['startDate'], args['endDate'], args['uName'], args['uFileName'], args['vName'], args['vFileName'], args['bName'], args['bFileName'])
            return 201


    def put(self):
            args = parser.parse_args()
            updateObservation(args['id'], args['name'], args['startDate'], args['endDate'], args['uName'], args['uFileName'], args['vName'], args['vFileName'], args['bName'], args['bFileName'])
            return 201




class RestLastObservation(Resource):
    def get(self):
            return REST["lastLoad"]


    def put(self):
        procRunner()
        print threading.current_thread()
        for t in threading.enumerate():
            if t is threading.enumerate():
                continue
            logging.debug('joining %s', t.getName())
            t.join(2.0)
            print 't.isAlive()', t.isAlive()
        #procRunner()
        return LastLoad



class RestDeleteObservation(Resource):
    def post(self):
            args = parser.parse_args()
            deleteObservation(args['id'])
            return 201



class RestObservationHRDiagram(Resource):
    def get(self):
            return REST["observationsHRDiagram"]



class RestObservationDiagram(Resource):
    def get(self):
            return REST["observationsDiagram"]

class RestFileUpload(Resource):
    def post(self):
            file = request.files['file']
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 201

class RestRegister(Resource):
    def post(self):
        args = parser.parse_args()
        addUser(args['name'],args['email'], args['password'])
        msg = Message("Hello "+args['name'],
                      sender="admin@astroApp.com",
                      recipients=[args['email']])
        mail.send(msg);
        return 201

class RestLogin(Resource):
    def put(self):
        args = parser.parse_args()
        print 'test'
        msg = verifyCredentials(args['email'], args['password'])
        return jsonify({'msg': msg})


api.add_resource(Rest, '/<rest_id>')
api.add_resource(RestObservation, '/observations')
api.add_resource(RestLastObservation, '/lastLoad')
api.add_resource(RestDeleteObservation, '/deletedObservations')
api.add_resource(RestObservationDiagram, '/observationsDiagram')
api.add_resource(RestObservationHRDiagram, '/observationsHRDiagram')
api.add_resource(RestFileUpload, '/fileUpload')
api.add_resource(RestRegister, '/register')
api.add_resource(RestLogin, '/login')

# Handling COR requests
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add("Access-Control-Max-Age", "3600");
    response.headers.add("Access-Control-Allow-Headers", "x-requested-with");
    response.headers.add("Connection", "keep-alive");
    response.headers.add("Vary", "Accept-Encoding");
    return response

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def f():
    t = threading.currentThread()
    r = random.randint(1,1)
    logging.debug('sleeping %s', r)
    time.sleep(r)
    logging.debug('ending')
    return

if __name__ == '__main__':
    #app.run(host=serverAddress, port=5000, threaded=True, use_reloader=True, reloader_type='watchdog')
    app.run(debug=True, host=serverAddress, port=5000, threaded=True)
    #app.run(debug=True, host=serverAddress, port=5000)

    for i in range(1):
        t = threading.Thread(target=f)
    t.setDaemon(True)
    t.start()


    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        logging.debug('joining %s', t.getName())
        t.join(2.0)
        print 't.isAlive()', t.isAlive()