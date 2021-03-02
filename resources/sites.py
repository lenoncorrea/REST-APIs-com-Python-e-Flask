from flask_restful import Resource, reqparse
from models.site import SiteModel
from flask_jwt_extended import jwt_required

class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self, id):
        site = SiteModel.find_site_by_id(id)
        if site:
            return site.json()
        return {'message': 'Site not found'}, 404

    @jwt_required()
    def delete(self, id):
        site = SiteModel.find_site_by_id(id)
        if site:
            site.delete_site()
            return {'message': 'Site deleted'}, 204
        return {'message': 'Site not found'}, 404
        
class SiteRegister(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('name', type=str, required=True, help='The field name cannot be empty')
    arguments.add_argument('url', type=str, required=True, help='The field url cannot be empty')

    @jwt_required()
    def post(self):
        data = SiteRegister.arguments.parse_args()
        site = SiteModel(**data)
        if SiteModel.find_site_by_name(site.name) or SiteModel.find_site_by_url(site.url):
            return {'message': 'Site already exists'}, 400
        try:
            site.save_site()
        except:
            return {'message': 'An internal error ocurred tryibg to create a new site'}, 500
        return site.json(), 201