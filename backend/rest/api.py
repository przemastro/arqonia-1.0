# coding: utf-8

from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory
from flask_restful import reqparse, Api, Resource, abort
from jsonBuilder import json_data, json_load, json_hrDiagramRange, json_hrdiagram, json_statistics, \
    json_lcDiagramRange, json_lcDiagram, userObservations, personalizedObservationsHRDiagram, personalizedObservationsHRDiagramRange, \
    personalizedLCDiagram, personalizedLCDiagramRange
from jsonParser import json_parser, updateObservation, addUser, verifyCredentials, objectDetails, addSubscriber, catalogData, \
    getPassword, updateUser, removeUser, addReductionImages, processImages, authentication, logoutUser, returnZippedImages, \
    addPhotometryData, deleteReductionImages
from procRunner import procRunner, deleteObservation, procPersonalizedRunner
import os
import ConfigParser
from threading import *
from flask_mail import Mail, Message
from sjcl import SJCL
import simplejson as json
import logging




app = Flask(__name__)

config = ConfigParser.RawConfigParser()
config.read('../resources/env.properties')

#app.config['MAIL_SERVER']='smtp.gmail.com'
#app.config['MAIL_PORT'] = 465
#app.config['MAIL_USERNAME'] = 'HRHomeSurvey@gmail.com'
#app.config['MAIL_PASSWORD'] = config.get('Mail', 'mail.hrhomesurveyPassword');
#app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = True

app.config['MAIL_SERVER']='arqonia.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'admin@arqonia.com'
app.config['MAIL_PASSWORD'] = config.get('Mail', 'mail.arqoniaPassword');
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False

mail = Mail()
mail.init_app(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['INPUT_FITS'] = 'inputFits/'
api = Api(app)




serverAddress = config.get('Server', 'server.address');
serverPort = int(config.get('Server', 'server.port'));
serverService = config.get('Server', 'server.service');
key = config.get('SecurityKey', 'public.key');


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
parser.add_argument('oldEmail', type=str)
parser.add_argument('password', type=str)
parser.add_argument('objectType', type=str)
parser.add_argument('verified', type=str)
parser.add_argument('abbreviation', type=str)
parser.add_argument('hrDiagramType', type=str)
parser.add_argument('filter', type=str)
parser.add_argument('activeNumber', type=str)
parser.add_argument('sessionId', type=str)
parser.add_argument('files', type=str, action='append')
parser.add_argument('conversionType', type=str)
parser.add_argument('imageType', type=str)
parser.add_argument('r1', type=str)
parser.add_argument('r2', type=str)
parser.add_argument('r3', type=str)
parser.add_argument('xCoordinate', type=str)
parser.add_argument('yCoordinate', type=str)
parser.add_argument('julianDate', type=str)
parser.add_argument('shift', type=str)
parser.add_argument('objectDistance', type=str)

#public
class Rest(Resource):
    def get(self, rest_id):
            abort_if_json_doesnt_exist(rest_id)
            return REST[rest_id]

#private
class RestUserObservation(Resource):
    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           observations = userObservations(args['email'])
           return jsonify(observations)
        else:
           observations = []
           return observations, 401

#private
class RestObservation(Resource):
    def post(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           json_parser(args['name'], args['startDate'], args['endDate'], args['uFileName'],
                       args['vFileName'], args['bFileName'], args['rFileName'], args['iFileName'],
                       args['objectType'], args['verified'], args['email'])
           content = Message("New Observation Added",
                             sender="admin@arqonia.com",
                             recipients=[args['email']])
           content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> New Observation Added </div>' \
                          '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                          'Hi, <br><br>You have added '+args['name']+' to the staging area.<br>Follow the link to verify results: <a href="http://arqonia.com/table-list" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'
           mail.send(content);
           return 201
        else:
           data = []
           return data, 401

    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           updateObservation(args['id'], args['name'], args['startDate'], args['endDate'], args['uFileName'],
                             args['vFileName'], args['bFileName'], args['rFileName'], args['iFileName'],
                             args['objectType'], args['verified'], args['email'])
           content = Message("Existing Observation Updated",
                             sender="admin@arqonia.com",
                             recipients=[args['email']])
           content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Existing Observation Updated </div>' \
                          '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                          'Hi, <br><br>You have updated '+args['name']+' in the staging area.<br>Follow the link to verify results: <a href="http://arqonia.com/table-list" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'
           mail.send(content);
           return 201
        else:
            data = []
            return data, 401



#admin
class RestLastObservation(Resource):
    def get(self):
            return REST["lastLoad"]


    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           procRunner()
           os.system("forceKill.bat")
           return 201
        else:
            data = []
            return data, 401

#private
class RestUserProcessData(Resource):
    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           procPersonalizedRunner(args['email'])
           return 201
        else:
            data = []
            return data, 401

#private
class RestDeleteObservation(Resource):
    def post(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           deleteObservation(args['id'])
           content = Message("Existing Observation Removed",
                             sender="admin@arqonia.com",
                             recipients=[args['email']])
           content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Existing Observation Removed </div>' \
                          '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                          'Hi, <br><br>You have removed '+args['name']+' from the staging area.<br>Follow the link to verify results: <a href="http://arqonia.com/table-list" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'
           mail.send(content);
           return 201
        else:
            data = []
            return data, 401


#Personalized HR Diagrams Data
#private
class RestPersonalizedObservationHRDiagram(Resource):
    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           data = personalizedObservationsHRDiagram(args['hrDiagramType'], args['email'])
           return jsonify(data)
        else:
           data = []
           return data, 401


#Personalized HR Diagrams Data Range
#private
class RestPersonalizedObservationHRDiagramRange(Resource):
    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           data = personalizedObservationsHRDiagramRange(args['hrDiagramType'], args['email'])
           return jsonify(data)
        else:
           data = []
           return data, 401

#Personalized LC Diagrams Data
#private
class RestPersonalizedObservationLCDiagram(Resource):
    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           data = personalizedLCDiagram(args['filter'], args['email'])
           return jsonify(data)
        else:
           data = []
           return data, 401


#Personalized LC Diagrams Range
#private
class RestPersonalizedObservationLCDiagramRange(Resource):
    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           data = personalizedLCDiagramRange(args['filter'], args['email'])
           return jsonify(data)
        else:
           data = []
           return data, 401

#public
#HR Diagrams Data
class RestObservationBVDiagram(Resource):
    def get(self):
            return REST["observationsBVDiagram"]

#public
class RestObservationUBDiagram(Resource):
    def get(self):
        return REST["observationsUBDiagram"]

#public
class RestObservationVIDiagram(Resource):
    def get(self):
        return REST["observationsVIDiagram"]

#public
class RestObservationRIDiagram(Resource):
    def get(self):
        return REST["observationsRIDiagram"]


#HR Diagrams Range
#public
class RestObservationBVDiagramRange(Resource):
    def get(self):
            return REST["observationsBVDiagramRange"]

#public
class RestObservationUBDiagramRange(Resource):
    def get(self):
        return REST["observationsUBDiagramRange"]

#public
class RestObservationRIDiagramRange(Resource):
    def get(self):
        return REST["observationsRIDiagramRange"]

#public
class RestObservationVIDiagramRange(Resource):
    def get(self):
        return REST["observationsVIDiagramRange"]


#LC Diagrams Data
#public
class RestObservationLCUDiagram(Resource):
    def get(self):
        return REST["observationsLCUDiagram"]
#public
class RestObservationLCVDiagram(Resource):
    def get(self):
        return REST["observationsLCVDiagram"]

#public
class RestObservationLCBDiagram(Resource):
    def get(self):
        return REST["observationsLCBDiagram"]

#public
class RestObservationLCRDiagram(Resource):
    def get(self):
        return REST["observationsLCRDiagram"]

#public
class RestObservationLCIDiagram(Resource):
    def get(self):
        return REST["observationsLCIDiagram"]

#LC Diagrams Range
#public
class RestObservationLCUDiagramRange(Resource):
    def get(self):
        return REST["observationsLCUDiagramRange"]

#public
class RestObservationLCVDiagramRange(Resource):
    def get(self):
        return REST["observationsLCVDiagramRange"]

#public
class RestObservationLCBDiagramRange(Resource):
    def get(self):
        return REST["observationsLCBDiagramRange"]

#public
class RestObservationLCRDiagramRange(Resource):
    def get(self):
        return REST["observationsLCRDiagramRange"]

#public
class RestObservationLCIDiagramRange(Resource):
    def get(self):
        return REST["observationsLCIDiagramRange"]

#private
class RestFileUpload(Resource):
    def post(self):
        emailHeader = request.headers.get("Email")
        sessionIdHeader = request.headers.get("SessionId")
        auth = basicAuthentication(emailHeader, sessionIdHeader)
        if(auth == 'true'):
           file = request.files['file']
           filename = file.filename
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           return 201
        else:
            data = []
            return data, 401

#private
class RestInputFITSUpload(Resource):
    def post(self):
        emailHeader = request.headers.get("Email")
        sessionIdHeader = request.headers.get("SessionId")
        auth = basicAuthentication(emailHeader, sessionIdHeader)
        if(auth == 'true'):
           files = request.files.getlist("files")
           for file in files:
              filename = file.filename
              file.save(os.path.join(app.config['INPUT_FITS'], filename))
           return 201
        else:
            data = []
            return data, 401


#public
class RestRegister(Resource):
    def post(self):
        args = parser.parse_args()
        decrypted = decrypt_password(args['activeNumber'])
        msg = addUser(args['name'],args['email'], args['activeNumber'])
        if msg == 'Correct':
            content = Message("Hello "+args['name'],
                      sender="admin@arqonia.com",
                      recipients=[args['email']])
            content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Hello </div>' \
                           '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                           'Welcome '+args['name']+',<br><br>Thank you for joining Arqonia, the biggest astronomical fandom in the Universe. <br>Please login with following password to activate your account: <b style="color:red">'+decrypted+'</b><br>Follow the link to log in to the application: <a href="http://arqonia.com/main" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'
            mail.send(content);
        return jsonify({'msg': msg})

#private
class RestUpdateProfile(Resource):
    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['oldEmail'], args['sessionId'])
        if(auth == 'true'):
           msg = updateUser(args['name'],args['email'], args['password'],args['oldEmail'])
           if msg == 'Correct':
               content = Message("Profile Updated", sender="admin@arqonia.com", recipients=[args['email']])
               content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Profile Updated </div>' \
                              '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                              'Hi '+args['name']+',<br><br>Your Profile has been updated.<br>Follow the link to log in to the application: <a href="http://arqonia.com/main" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'
           mail.send(content);
           return jsonify({'msg': msg})
        else:
            data = []
            return data, 401

#private
class RestRemoveAccount(Resource):
    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           msg = removeUser(args['email'])
           if msg == 'Correct':
               content = Message("Goodbye",
                                 sender="admin@arqonia.com",
                                 recipients=[args['email']])
               content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Goodbye! </div>' \
                              '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                              'Hi, <br><br>Thank you for using Arqonia. <br>In order to remove your account permanently please ask <a style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;" href="mailto:admin@arqonia.com">Admin</a>. <br>We hope you will be back soon. </b><br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'
               mail.send(content);
           return jsonify({'msg': msg})
        else:
            data = []
            return data, 401

#public
class RestReminder(Resource):
    def post(self):
        args = parser.parse_args()
        msg = getPassword(args['email'])
        msg = decrypt_password(msg)
        content = Message("Password Reminder", sender="admin@arqonia.com", recipients=[args['email']])
        content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Password Reminder </div>' \
                       '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                       'Hi, <br><br>This is reply to your request. <br><br>Your password is: <b style="color:red"> '+msg+' </b><br>Follow the link to log in to the application: <a href="http://arqonia.com/main" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'
        mail.send(content);
        return 201

#public
class RestLogin(Resource):
    def put(self):
        args = parser.parse_args()
        sj = decrypt_password(args['password'])
        msg = verifyCredentials(args['email'], sj, args['sessionId'])
        return jsonify({'msg': msg})

#private
class RestLogout(Resource):
    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           logoutUser(args['email'])
           return 201
        else:
            data = []
            return data, 401

#public
class RestSearch(Resource):
    def put(self):
        args = parser.parse_args()
        details = objectDetails(args['name'])
        return jsonify(details)

#public
class RestStatistics(Resource):
    def get(self):
        return REST["statistics"]

#public
class RestSubscribe(Resource):
    def post(self):
        args = parser.parse_args()
        addSubscriber(args['email'])
        return 201

#private
class RestCatalog(Resource):
    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           catalog = catalogData(args['objectType'], args['abbreviation'], args['email'])
           return jsonify(catalog)
        else:
            data = []
            return data, 401

#private
class RestReductionImages(Resource):
    def post(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           args = parser.parse_args()
           data = addReductionImages(args['sessionId'], args['files'], args['email'], args['conversionType'], args['imageType'])
           return jsonify(data)
        else:
            data = []
            return data, 401

#private
class RestDeleteReductionImages(Resource):
    def post(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
            args = parser.parse_args()
            deleteReductionImages(args['sessionId'], args['imageType'])
            return 201
        else:
            data = []
            return data, 401

#private
class RestProcessImages(Resource):
    def post(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
           data = processImages(args['sessionId'], args['email'])
           return jsonify(data)
        else:
            data = []
            return data, 401

#private
class RestSaveImages(Resource):
    def post(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
            returnZippedImages(args['sessionId'], args['email'])
            return 201
        else:
            data = []
            return data, 401

#private
class RestAddPhotometry(Resource):
    def put(self):
        args = parser.parse_args()
        auth = basicAuthentication(args['email'], args['sessionId'])
        if(auth == 'true'):
            data = addPhotometryData(args['xCoordinate'], args['yCoordinate'], args['r1'], args['r2'], args['r3'],
                                     args['julianDate'], args['shift'], args['sessionId'], args['objectDistance'])
            return jsonify(data)
        else:
            data = []
            return data, 401

def basicAuthentication(email, sessionId):
    if(str(sessionId) != 'None'):
       auth = authentication(email, sessionId)
    else:
       auth = 'false'
    return auth


api.add_resource(Rest, '/<rest_id>')
api.add_resource(RestObservation, '/observations')
api.add_resource(RestUserObservation, '/userObservations')
api.add_resource(RestLastObservation, '/lastLoad')
api.add_resource(RestUserProcessData, '/processUserData')
api.add_resource(RestDeleteObservation, '/deletedObservations')
api.add_resource(RestPersonalizedObservationHRDiagramRange, '/RestPersonalizedObservationHRDiagramRange')
api.add_resource(RestPersonalizedObservationHRDiagram, '/RestPersonalizedObservationHRDiagram')
api.add_resource(RestPersonalizedObservationLCDiagramRange, '/RestPersonalizedLCDiagramRange')
api.add_resource(RestPersonalizedObservationLCDiagram, '/RestPersonalizedLCDiagram')
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
api.add_resource(RestInputFITSUpload, '/inputFits')
api.add_resource(RestRegister, '/register')
api.add_resource(RestUpdateProfile, '/updateProfile')
api.add_resource(RestRemoveAccount, '/removeAccount')
api.add_resource(RestReminder, '/reminder')
api.add_resource(RestLogin, '/login')
api.add_resource(RestLogout, '/logout')
api.add_resource(RestSearch, '/search')
api.add_resource(RestStatistics, '/statistics')
api.add_resource(RestSubscribe, '/subscribe')
api.add_resource(RestCatalog, '/catalog')
api.add_resource(RestReductionImages, '/reductionImages')
api.add_resource(RestDeleteReductionImages, '/deleteReductionImages')
api.add_resource(RestProcessImages, '/processImages')
api.add_resource(RestSaveImages, '/saveImages')
api.add_resource(RestAddPhotometry, '/photometry')


# Handling COR requests
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,SessionId,Email')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add("Access-Control-Max-Age", "3600");
    response.headers.add("Access-Control-Allow-Headers", "x-requested-with");
    response.headers.add("Connection", "keep-alive");
    response.headers.add("Vary", "Accept-Encoding");
    return response



def decrypt_password(password):
    d = json.loads(password)
    sj = SJCL().decrypt(d, key)
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

