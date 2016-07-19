from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory
from flask_restful import reqparse, Api, Resource, abort
from jsonBuilder import json_data, json_load, json_diagram, json_hrdiagram
from jsonParser import json_parser, updateObservation, addUser, verifyCredentials
from procRunner import procRunner, deleteObservation
import os
import ConfigParser
import random
from threading import *
from flask_mail import Mail, Message
from sjcl import SJCL
import simplejson as json
import threading
import time
import logging
import win32serviceutil
import sys



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
config.read('../resources/env.properties')
serverAddress = config.get('Server', 'server.address');
serverPort = int(config.get('Server', 'server.port'));
serverService = config.get('Server', 'server.service');

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
        if serverService == 'Yes':
           #shutdown_server()
           #time.sleep(5)
           os.system("forceKill.bat")
           #win32serviceutil.RestartService("apipy")
           #sys.exit("Error message")
        return 'Processing...'

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

        sj = decrypt_password(args['password'])
        msg = addUser(args['name'],args['email'], str(sj))
        if msg == 'Correct':
            content = Message("Hello "+args['name'],
                      sender="admin@astroApp.com",
                      recipients=[args['email']])
            content.body = 'Welcome '+args['name']+',\n\nThank you for joining AstroApp, the biggest astronomical fandom in the Universe.' \
                                                   '\n\nBest Regards, \nThe Creator'
            mail.send(content);
        return jsonify({'msg': msg})


class RestLogin(Resource):
    def put(self):
        args = parser.parse_args()
        sj = decrypt_password(args['password'])
        msg = verifyCredentials(args['email'], sj)
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



def decrypt_password(password):
    d = json.loads(password)
    sj = SJCL().decrypt(d, "password")
    return sj

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)



def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    app.run(debug=False, host=serverAddress, port=serverPort, threaded=True, use_reloader=True)
    #app.run(debug=True, host=serverAddress, port=serverPort, threaded=True)
    #app.run(debug=True, host=serverAddress, port=serverPort)

