from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource, abort
from jsonBuilder import json_data, json_load, json_diagram, json_hrdiagram
from jsonParser import json_parser, updateObservation
from procRunner import procRunner, deleteObservation


app = Flask(__name__)
api = Api(app)

json_data()
json_load()
json_diagram()
json_hrdiagram()

Observations = json_data.jsonData
LastLoad = json_load.jsonLastLoad
ObservationsDiagram = json_diagram.jsonDiagram
ObservationsHRDiagram = json_hrdiagram.jsonHRDiagram

#print Observations
#print LastLoad

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
parser.add_argument('uFileName', type=str)
parser.add_argument('vPhotometry', type=str)
parser.add_argument('bPhotometry', type=str)
parser.add_argument('id', type=str)

class Rest(Resource):
    def get(self, rest_id):
        abort_if_json_doesnt_exist(rest_id)
        return REST[rest_id]


class RestObservation(Resource):
    def post(self):
        args = parser.parse_args()
        json_parser(args['name'], args['startDate'], args['endDate'], args['uFileName'], args['vPhotometry'], args['bPhotometry'])
        return 201

    def put(self):
        args = parser.parse_args()
        updateObservation(args['id'], args['name'], args['startDate'], args['endDate'], args['uFileName'], args['vPhotometry'], args['bPhotometry'])
        return 201


class RestLastObservation(Resource):
    def get(self):
        return REST["lastLoad"]

    def put(self):
        procRunner()
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


api.add_resource(Rest, '/<rest_id>')
api.add_resource(RestObservation, '/observations')
api.add_resource(RestLastObservation, '/lastLoad')
api.add_resource(RestDeleteObservation, '/deletedObservations')
api.add_resource(RestObservationDiagram, '/observationsDiagram')
api.add_resource(RestObservationHRDiagram, '/observationsHRDiagram')

# Handling COR requests
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add("Access-Control-Max-Age", "3600");
    response.headers.add("Access-Control-Allow-Headers", "x-requested-with");
    response.headers.add("Connection", "keep-alive");
    return response


if __name__ == '__main__':
    app.run(debug=True)
