from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class urlArguments():

    def urlBeerDetails(self):
        parser = reqparse.RequestParser()
        #beer id to be used with beer details
        parser.add_argument('beer_id', type=int, required=True)
        args = parser.parse_args()
        return args['beer_id']

    def urlBeerPrice(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', type=str, required=True)
        parser.add_argument('beer_name', type=str, required=True)
        parser.add_argument('beer_price', type=float, required=True)
        parser.add_argument('latitude', type=str, required=True)
        parser.add_argument('longitude', type=str, required=True)
        parser.add_argument('units', type=int, required=True)
        args = parser.parse_args()
        return args

    def urlFindBeer(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', type=str, required=True)
        parser.add_argument('latitude', type=str, required=True)
        parser.add_argument('longitude', type=str, required=True)
        parser.add_argument('searchBy', type=str, required=True)
        parser.add_argument('userSearchInput', type=str, required=True)
        args = parser.parse_args()
        return args



    def urlAddUser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userName', type=str, required=True)
        parser.add_argument('userPassword', type=str, required=True)
        parser.add_argument('emailAddress', type=str,required=True)
        parser.add_argument('userAge', type=int, required=True)
        parser.add_argument('userGender', type=str, required=True)
        parser.add_argument('maxTravelDistance', type=int, required=True)
        parser.add_argument('latitude', type=str, required=True)
        parser.add_argument('longitude', type=str, required=True)
        args = parser.parse_args()
        return args

    def urlLogin(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userName', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        return args

    def urlBeerStaging(self):
        parser = reqparse.RequestParser()
        parser.add_argument('beer_id', type=int, required=True)
        parser.add_argument('beer_price', type=float, required=True)
        parser.add_argument('units', type=int, required=True)
        parser.add_argument('latitude', type=str, required=True)
        parser.add_argument('longitude', type=str, required=True)
        args = parser.parse_args
        return args