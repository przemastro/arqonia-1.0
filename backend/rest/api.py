from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory
from flask_restful import reqparse, Api, Resource, abort
from jsonBuilder import json_data, json_load, json_hrDiagramRange, json_hrdiagram, json_statistics, json_lcDiagramRange, json_lcDiagram
from jsonParser import json_parser, updateObservation, addUser, verifyCredentials, objectDetails, addSubscriber, catalogData
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
json_hrDiagramRange()
json_hrdiagram()
json_statistics()
json_lcDiagramRange()
json_lcDiagram()

Observations = json_data.jsonData
LastLoad = json_load.jsonLastLoad
ObservationsBVDiagramRange = json_hrDiagramRange.jsonBVDiagramRange
ObservationsUBDiagramRange = json_hrDiagramRange.jsonUBDiagramRange
ObservationsRIDiagramRange = json_hrDiagramRange.jsonRIDiagramRange
ObservationsVIDiagramRange = json_hrDiagramRange.jsonVIDiagramRange

ObservationsBVDiagram = json_hrdiagram.jsonBVDiagram
ObservationsUBDiagram = json_hrdiagram.jsonUBDiagram
ObservationsRIDiagram = json_hrdiagram.jsonRIDiagram
ObservationsVIDiagram = json_hrdiagram.jsonVIDiagram

Statistics = json_statistics.jsonStatistics

ObservationsLCUDiagramRange = json_lcDiagramRange.jsonLCUDiagramRange
ObservationsLCVDiagramRange = json_lcDiagramRange.jsonLCVDiagramRange
ObservationsLCBDiagramRange = json_lcDiagramRange.jsonLCBDiagramRange
ObservationsLCRDiagramRange = json_lcDiagramRange.jsonLCRDiagramRange
ObservationsLCIDiagramRange = json_lcDiagramRange.jsonLCIDiagramRange

ObservationsLCUDiagram = json_lcDiagram.jsonLCUDiagram
ObservationsLCVDiagram = json_lcDiagram.jsonLCVDiagram
ObservationsLCBDiagram = json_lcDiagram.jsonLCBDiagram
ObservationsLCRDiagram = json_lcDiagram.jsonLCRDiagram
ObservationsLCIDiagram = json_lcDiagram.jsonLCIDiagram

REST = {'observations': Observations,
        'lastLoad': LastLoad,
        'observationsBVDiagramRange': ObservationsBVDiagramRange,
        'observationsUBDiagramRange': ObservationsUBDiagramRange,
        'observationsRIDiagramRange': ObservationsRIDiagramRange,
        'observationsVIDiagramRange': ObservationsVIDiagramRange,
        'observationsBVDiagram': ObservationsBVDiagram,
        'observationsUBDiagram': ObservationsUBDiagram,
        'observationsRIDiagram': ObservationsRIDiagram,
        'observationsVIDiagram': ObservationsVIDiagram,
        'statistics': Statistics,
        'observationsLCUDiagramRange': ObservationsLCUDiagramRange,
        'observationsLCVDiagramRange': ObservationsLCVDiagramRange,
        'observationsLCBDiagramRange': ObservationsLCBDiagramRange,
        'observationsLCRDiagramRange': ObservationsLCRDiagramRange,
        'observationsLCIDiagramRange': ObservationsLCIDiagramRange,
        'observationsLCUDiagram': ObservationsLCUDiagram,
        'observationsLCVDiagram': ObservationsLCVDiagram,
        'observationsLCBDiagram': ObservationsLCBDiagram,
        'observationsLCRDiagram': ObservationsLCRDiagram,
        'observationsLCIDiagram': ObservationsLCIDiagram
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
parser.add_argument('rName', type=str)
parser.add_argument('rFileName', type=str)
parser.add_argument('iName', type=str)
parser.add_argument('iFileName', type=str)
parser.add_argument('id', type=str)
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)
parser.add_argument('objectType', type=str)
parser.add_argument('verified', type=str)



class Rest(Resource):
    def get(self, rest_id):
            abort_if_json_doesnt_exist(rest_id)
            return REST[rest_id]


class RestObservation(Resource):
    def post(self):
            args = parser.parse_args()
            json_parser(args['name'], args['startDate'], args['endDate'], args['uFileName'],
                        args['vFileName'], args['bFileName'], args['rFileName'], args['iFileName'],
                        args['objectType'], args['verified'])
            return 201

    def put(self):
            args = parser.parse_args()
            updateObservation(args['id'], args['name'], args['startDate'], args['endDate'], args['uFileName'],
                              args['vFileName'], args['bFileName'], args['rFileName'], args['iFileName'],
                              args['objectType'], args['verified'])
            return 201




class RestLastObservation(Resource):
    def get(self):
            return REST["lastLoad"]


    def put(self):
        procRunner()
        #if serverService == 'Yes':
           #shutdown_server()
        #   time.sleep(1000)
        os.system("forceKill.bat")
        return 201

class RestDeleteObservation(Resource):
    def post(self):
            args = parser.parse_args()
            deleteObservation(args['id'])
            return 201


#HR Diagrams Data
class RestObservationBVDiagram(Resource):
    def get(self):
            return REST["observationsBVDiagram"]

class RestObservationUBDiagram(Resource):
    def get(self):
        return REST["observationsUBDiagram"]

class RestObservationVIDiagram(Resource):
    def get(self):
        return REST["observationsVIDiagram"]

class RestObservationRIDiagram(Resource):
    def get(self):
        return REST["observationsRIDiagram"]

#HR Diagrams Range
class RestObservationBVDiagramRange(Resource):
    def get(self):
            return REST["observationsBVDiagramRange"]

class RestObservationUBDiagramRange(Resource):
    def get(self):
        return REST["observationsUBDiagramRange"]

class RestObservationRIDiagramRange(Resource):
    def get(self):
        return REST["observationsRIDiagramRange"]

class RestObservationVIDiagramRange(Resource):
    def get(self):
        return REST["observationsVIDiagramRange"]


#LC Diagrams Data
class RestObservationLCUDiagram(Resource):
    def get(self):
        return REST["observationsLCUDiagram"]

class RestObservationLCVDiagram(Resource):
    def get(self):
        return REST["observationsLCVDiagram"]

class RestObservationLCBDiagram(Resource):
    def get(self):
        return REST["observationsLCBDiagram"]

class RestObservationLCRDiagram(Resource):
    def get(self):
        return REST["observationsLCRDiagram"]

class RestObservationLCIDiagram(Resource):
    def get(self):
        return REST["observationsLCIDiagram"]

#LC Diagrams Range
class RestObservationLCUDiagramRange(Resource):
    def get(self):
        return REST["observationsLCUDiagramRange"]

class RestObservationLCVDiagramRange(Resource):
    def get(self):
        return REST["observationsLCVDiagramRange"]

class RestObservationLCBDiagramRange(Resource):
    def get(self):
        return REST["observationsLCBDiagramRange"]

class RestObservationLCRDiagramRange(Resource):
    def get(self):
        return REST["observationsLCRDiagramRange"]

class RestObservationLCIDiagramRange(Resource):
    def get(self):
        return REST["observationsLCIDiagramRange"]


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

class RestSearch(Resource):
    def put(self):
        args = parser.parse_args()
        details = objectDetails(args['name'])
        print details
        return jsonify(details)

class RestStatistics(Resource):
    def get(self):
        return REST["statistics"]

class RestSubscribe(Resource):
    def post(self):
        args = parser.parse_args()
        addSubscriber(args['email'])
        return 201


class RestCatalog(Resource):
    def put(self):
        args = parser.parse_args()
        catalog = catalogData(args['objectType'])
        print catalogData
        return jsonify(catalog)


api.add_resource(Rest, '/<rest_id>')
api.add_resource(RestObservation, '/observations')
api.add_resource(RestLastObservation, '/lastLoad')
api.add_resource(RestDeleteObservation, '/deletedObservations')
api.add_resource(RestObservationBVDiagramRange, '/observationsBVDiagramRange')
api.add_resource(RestObservationUBDiagramRange, '/observationsUBDiagramRange')
api.add_resource(RestObservationRIDiagramRange, '/observationsRIDiagramRange')
api.add_resource(RestObservationVIDiagramRange, '/observationsVIDiagramRange')
api.add_resource(RestObservationBVDiagram, '/observationsBVDiagram')
api.add_resource(RestObservationUBDiagram, '/observationsUBDiagram')
api.add_resource(RestObservationRIDiagram, '/observationsRIDiagram')
api.add_resource(RestObservationVIDiagram, '/observationsVIDiagram')
api.add_resource(RestObservationLCUDiagramRange, '/observationsLCUDiagramRange')
api.add_resource(RestObservationLCVDiagramRange, '/observationsLCVDiagramRange')
api.add_resource(RestObservationLCBDiagramRange, '/observationsLCBDiagramRange')
api.add_resource(RestObservationLCRDiagramRange, '/observationsLCRDiagramRange')
api.add_resource(RestObservationLCIDiagramRange, '/observationsLCIDiagramRange')
api.add_resource(RestObservationLCUDiagram, '/observationsLCUDiagram')
api.add_resource(RestObservationLCVDiagram, '/observationsLCVDiagram')
api.add_resource(RestObservationLCBDiagram, '/observationsLCBDiagram')
api.add_resource(RestObservationLCRDiagram, '/observationsLCRDiagram')
api.add_resource(RestObservationLCIDiagram, '/observationsLCIDiagram')
api.add_resource(RestFileUpload, '/fileUpload')
api.add_resource(RestRegister, '/register')
api.add_resource(RestLogin, '/login')
api.add_resource(RestSearch, '/search')
api.add_resource(RestStatistics, '/statistics')
api.add_resource(RestSubscribe, '/subscribe')
api.add_resource(RestCatalog, '/catalog')


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

