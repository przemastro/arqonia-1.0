from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource, abort
from jsonBuilder import json_data


app = Flask(__name__)
api = Api(app)

json_data()

Observations = json_data.jsonData

print Observations

REST = {'observations': Observations
        }


def abort_if_json_doesnt_exist(rest_id):
    if rest_id not in REST:
        abort(404, message="Deeply sorry but Json {} doesn't exist".format(rest_id))


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)

class Rest(Resource):
    def get(self, rest_id):
        abort_if_json_doesnt_exist(rest_id)
        return REST[rest_id]

api.add_resource(Rest, '/<rest_id>')

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