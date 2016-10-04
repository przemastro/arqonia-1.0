# coding: utf-8

from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory
from flask_restful import reqparse, Api, Resource, abort
from jsonBuilder import json_data, json_load, json_hrDiagramRange, json_hrdiagram, json_statistics, \
    json_lcDiagramRange, json_lcDiagram, userObservations, personalizedObservationsHRDiagram, personalizedObservationsHRDiagramRange, \
    personalizedLCDiagram, personalizedLCDiagramRange
from jsonParser import json_parser, updateObservation, addUser, verifyCredentials, objectDetails, addSubscriber, catalogData, \
    getPassword, updateUser, removeUser
from procRunner import procRunner, deleteObservation, procPersonalizedRunner
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
app.config['INPUT_FITS'] = 'inputFits/'
api = Api(app)



config = ConfigParser.RawConfigParser()
config.read('../resources/env.properties')
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


class Rest(Resource):
    def get(self, rest_id):
            abort_if_json_doesnt_exist(rest_id)
            return REST[rest_id]


class RestUserObservation(Resource):
    def put(self):
        args = parser.parse_args()
        observations = userObservations(args['email'])
        return jsonify(observations)


class RestObservation(Resource):
    def post(self):
            args = parser.parse_args()
            print 'test'
            json_parser(args['name'], args['startDate'], args['endDate'], args['uFileName'],
                        args['vFileName'], args['bFileName'], args['rFileName'], args['iFileName'],
                        args['objectType'], args['verified'], args['email'])
            print 'test2'
            content = Message("New Observation Added",
                              sender="admin@arqonia.com",
                              recipients=[args['email']])
            #content.body = 'Hi,\n\nYou have added '+args['name']+' to the staging area.' \
            #                               '\n\nBest Regards, \nThe Creator'

            content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> New Observation Added </div>' \
                           '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                           'Hi, <br><br>You have added '+args['name']+' to the staging area.<br>Follow the link to verify results: <a href="http://arqonia.com/#/table-list" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'

            mail.send(content);
            return 201

    def put(self):
            args = parser.parse_args()
            updateObservation(args['id'], args['name'], args['startDate'], args['endDate'], args['uFileName'],
                              args['vFileName'], args['bFileName'], args['rFileName'], args['iFileName'],
                              args['objectType'], args['verified'], args['email'])
            content = Message("Existing Observation Updated",
                              sender="admin@arqonia.com",
                              recipients=[args['email']])
            #content.body = 'Hi,\n\nYou have updated '+args['name']+' in the staging area.' \
            #                                                     '\n\nBest Regards, \nThe Creator'
            content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Existing Observation Updated </div>' \
                           '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                           'Hi, <br><br>You have updated '+args['name']+' in the staging area.<br>Follow the link to verify results: <a href="http://arqonia.com/#/table-list" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'

            mail.send(content);
            return 201




class RestLastObservation(Resource):
    def get(self):
            return REST["lastLoad"]


    def put(self):
        procRunner()
        os.system("forceKill.bat")
        return 201

class RestUserProcessData(Resource):
    def put(self):
        args = parser.parse_args()
        procPersonalizedRunner(args['email'])
        return 201

class RestDeleteObservation(Resource):
    def post(self):
            args = parser.parse_args()
            deleteObservation(args['id'])
            content = Message("Existing Observation Removed",
                              sender="admin@arqonia.com",
                              recipients=[args['email']])
            #content.body = 'Hi,\n\nYou have removed '+args['name']+' from the staging area.' \
            #                                                       '\n\nBest Regards, \nThe Creator'
            content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Existing Observation Removed </div>' \
                           '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                           'Hi, <br><br>You have removed '+args['name']+' from the staging area.<br>Follow the link to verify results: <a href="http://arqonia.com/#/table-list" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'

            mail.send(content);
            return 201


#Personalized HR Diagrams Data
class RestPersonalizedObservationHRDiagram(Resource):
    def put(self):
        args = parser.parse_args()
        data = personalizedObservationsHRDiagram(args['hrDiagramType'], args['email'])
        time.sleep(1)
        return jsonify(data)


#Personalized HR Diagrams Data Range
class RestPersonalizedObservationHRDiagramRange(Resource):
    def put(self):
        args = parser.parse_args()
        data = personalizedObservationsHRDiagramRange(args['hrDiagramType'], args['email'])
        return jsonify(data)

#Personalized LC Diagrams Data
class RestPersonalizedObservationLCDiagram(Resource):
    def put(self):
        args = parser.parse_args()
        data = personalizedLCDiagram(args['filter'], args['email'])
        #time.sleep(1)
        return jsonify(data)

#Personalized LC Diagrams Range
class RestPersonalizedObservationLCDiagramRange(Resource):
    def put(self):
        args = parser.parse_args()
        data = personalizedLCDiagramRange(args['filter'], args['email'])
        return jsonify(data)

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

class RestInputFITSUpload(Resource):
    def post(self):
        file = request.files['file']
        print file
        filename = file.filename
        file.save(os.path.join(app.config['INPUT_FITS'], filename))
        return 201

class RestRegister(Resource):
    def post(self):
        args = parser.parse_args()

        decrypted = decrypt_password(args['activeNumber'])
        #msg = addUser(args['name'],args['email'], str(sj))
        msg = addUser(args['name'],args['email'], args['activeNumber'])
        if msg == 'Correct':
            content = Message("Hello "+args['name'],
                      sender="admin@arqonia.com",
                      recipients=[args['email']])
            #content.body = 'Welcome '+args['name']+',\n\nThank you for joining Arqonia, the biggest astronomical fandom in the Universe.' \
            #                                       '\nPlease login with following password to activate your account: '+decrypted+'' \
            #                                       '\n\nBest Regards, \nAdmin'
            content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Hello </div>' \
                           '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                           'Welcome '+args['name']+',<br><br>Thank you for joining Arqonia, the biggest astronomical fandom in the Universe. <br>Please login with following password to activate your account: <b style="color:red">'+decrypted+'</b><br>Follow the link to log in to the application: <a href="http://arqonia.com/#/main" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'

            mail.send(content);
        return jsonify({'msg': msg})


class RestUpdateProfile(Resource):
    def put(self):
        args = parser.parse_args()

        #sj = decrypt_password(args['password'])
        #msg = updateUser(args['name'],args['email'], str(sj),args['oldEmail'])
        msg = updateUser(args['name'],args['email'], args['password'],args['oldEmail'])
        if msg == 'Correct':
            content = Message("Profile Updated",
                              sender="admin@arqonia.com",
                              recipients=[args['email']])
            #content.body = 'Hi '+args['name']+',\n\nYour Profile has been updated.' \
            #                                       '\n\nBest Regards, \nAdmin'

            content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Profile Updated </div>' \
                           '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                           'Hi '+args['name']+',<br><br>Your Profile has been updated.<br>Follow the link to log in to the application: <a href="http://arqonia.com/#/main" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'

        mail.send(content);
        return jsonify({'msg': msg})

class RestRemoveAccount(Resource):
    def put(self):
        args = parser.parse_args()
        msg = removeUser(args['email'])
        if msg == 'Correct':
            content = Message("Goodbye",
                              sender="admin@arqonia.com",
                              recipients=[args['email']])
            #content.body = 'Hi, \n\nThank you for using Arqonia. We hope you will be back soon.' \
            #                                     '\n\nBest Regards, \nAdmin'

            content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Goodbye! </div>' \
                           '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                           'Hi, <br><br>Thank you for using Arqonia. <br>In order to remove your account permanently please ask <a style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;" href="mailto:admin@arqonia.com">Admin</a>. <br>We hope you will be back soon. </b><br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'

            mail.send(content);
        return jsonify({'msg': msg})

class RestReminder(Resource):
    def post(self):
        args = parser.parse_args()

        msg = getPassword(args['email'])
        msg = decrypt_password(msg)
        content = Message("Password Reminder",
                          sender="admin@arqonia.com",
                          recipients=[args['email']])
        #content.body = 'Hi,\n\nThis is reply for your request. \n\nYour password is: '+msg+'' \
        #                                       '\n\nBest Regards, \nAdmin'

        content.html = '<!DOCTYPE html><html lang="en"><meta charset="utf-8"><body style="background-color:white;margin-bottom: 50px;"><div style="max-width: 650px;height: 550px;border-style: solid;border-width: 1px;border-color: #EBEBEB; background-color:white;width:100%;margin: 40px auto;"> <div id="header" align="center" style="background-color: white;background-image: none; background-repeat: repeat;background-attachment: scroll;background-position: 0% 0%;background-clip: border-box; background-origin: padding-box;background-size: auto auto;width: 100%;margin:auto; position:relative;z-index: 1;text-align:right;margin-top:10px;"> <ul style="list-style-type: none;margin: 0;padding: 0;overflow: hidden;font-family: ''Helvetica Neue'', ''Helvetica'', Helvetica, Arial, sans-serif;border-bottom: 1px solid #4D9DC2 !important;width:91%;margin-left:30px"> <li style="text-align:center;margin-top: 10px;margin-bottom:10px;margin-left:0px;float: left;"> <a class="pageSection" style="color:white;text-decoration: none;color:#4D9DC2;font-size: 1.5rem;">A R Q O N I A</a></li></ul> </div><div align="center" style="background-color: white;position: relative;margin:auto;margin-top:30px;z-index: 0;height:40px;color:#4D9DC2;font-size: 1.8rem;"> Password Reminder </div>' \
                       '<div style="height:375px"> <p style="padding-left:50px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;color: #4c4c4c;font-style: normal;">' \
                       'Hi, <br><br>This is reply to your request. <br><br>Your password is: <b style="color:red"> '+msg+' </b><br>Follow the link to log in to the application: <a href="http://arqonia.com/#/main" style="text-decoration: none;color:#4D9DC2;padding-left:0px;padding-top:20px;font-family: inherit;font-weight: normal;font-size: 1.0rem;line-height: 1.6;margin-bottom: 1.25rem;text-rendering: optimizeLegibility;font-style: normal;">ARQONIA</a>  <br><br><br> Best Regards, <br>Arqonia Team<br><br><br>This is an automated email. Please do not reply.</p></div><div align="center" style="color: white;font-weight: 300;padding: 1px 0;background-color: #323232;font-size: 12px;max-width: 650px; background-color: #4D9DC2;height: 15px;margin-bottom: 0px;margin-top: 0px;width:91%;margin-left:30px"> ©2016 ARQONIA. All Rights Reserved. </div></div></body></html>'

        mail.send(content);
        return 201

class RestLogin(Resource):
    def put(self):
        args = parser.parse_args()
        sj = decrypt_password(args['password'])
        msg = verifyCredentials(args['email'], sj)
        #msg = verifyCredentials(args['email'], args['password'])
        return jsonify({'msg': msg})

class RestSearch(Resource):
    def put(self):
        args = parser.parse_args()
        details = objectDetails(args['name'])
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
        catalog = catalogData(args['objectType'], args['abbreviation'], args['email'])
        return jsonify(catalog)


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

