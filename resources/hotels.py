from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from resources.filters import FiltersResource
from flask_jwt_extended import jwt_required
import sqlite3
# import mysql.connector

path_params = reqparse.RequestParser()
path_params.add_argument('city', type=str)
path_params.add_argument('min_stars', type=float)
path_params.add_argument('max_stars', type=float)
path_params.add_argument('min_daily', type=float)
path_params.add_argument('max_daily', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Hotels(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        # connection = mysql.connector.connect(user='flask', password='flask', host='172.17.0.2', database='flask ')
        cursor = connection.cursor()
        data = path_params.parse_args()
        valid_data = {chave:data[chave] for chave in data if data[chave] is not None}
        params = FiltersResource.normalize_path_params(**valid_data)
        if not params.get('city'):
            consult = FiltersResource.consult_no_city()
            tupla = tuple([params[chave] for chave in params])
            cursor.execute(consult, tupla)
            result = cursor.fetchall()
        else:
            consult = FiltersResource.consult_with_city()
            tupla = tuple([params[chave] for chave in params])
            cursor.execute(consult, tupla)
            result = cursor.fetchall()
        hotels = []
        if result:
            for line in result:
                hotels.append({
                    'id':  line[0],
                    'name': line[1],
                    'stars': line[2],
                    'daily': line[3],
                    'state': line[4],
                    'city': line[5],
                    'site_id': line[6]
                })
        return {'hotels': hotels}
        # return {'hotels': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('name', type=str, required=True, help='The field name cannot be empty')
    arguments.add_argument('stars', type=float, required=True, help='The field stars cannot be empty')
    arguments.add_argument('daily', type=float)
    arguments.add_argument('state', type=str, required=True, help='The field state cannot be empty')
    arguments.add_argument('city', type=str, required=True, help='The field city cannot be empty')
    arguments.add_argument('site_id', type=int, required=True, help='Every hotel needs to be linked with a site')

    def get(self,id):
        hotel = HotelModel.hotel_find_by_id(id)
        if hotel:
            return hotel.json(), 200
        return {'message': 'Hotel not found'}, 404

    @jwt_required()
    def put(self,id):
        data = Hotel.arguments.parse_args()
        hotel = HotelModel.hotel_find_by_id(id)
        if hotel:
            hotel.update_hotel(**data)
            try:
                hotel.save_hotel()
            except:
                return {'message': 'An internal error ocurred trying to save hotel'}, 500
            return hotel.json(), 200
        hotel = HotelModel(id, **data)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel'}, 500
        return hotel.json(), 201
    
    @jwt_required()
    def delete(self,id):
        hotel = HotelModel.hotel_find_by_id(id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to save hotel'}, 500
            return {'message': 'Hotel deleted'}, 204
        return {'message': 'Hotel not found'}, 404

class HotelRegister(Resource):
    @jwt_required()
    def post(self):
        data = Hotel.arguments.parse_args()
        hotel = HotelModel(**data)
        if HotelModel.hotel_find_by_name(hotel.name):
            return {'message': 'Hotel already exists'}, 400
        if SiteModel.find_site_by_id(hotel.site_id) is None:
            return {'message': 'Site not exists'}, 400
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel'}, 500
        return hotel.json(), 201