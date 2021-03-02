from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models.user import UserModel
from models.blocklist import BlocklistModel
from sql_alchemy import banco
from werkzeug.security import safe_str_cmp
from datetime import datetime
from datetime import timezone
import traceback
from flask import make_response, render_template

arguments = reqparse.RequestParser()
arguments.add_argument('name', type=str)
arguments.add_argument('login', type=str, required=True, help='The field login cannot be empty')
arguments.add_argument('password', type=str, required=True, help='The field password cannot be empty')
arguments.add_argument('email', type=str)
arguments.add_argument('activate', type=bool)

class User(Resource):
    @jwt_required()
    def get(self, id):
        user = UserModel.user_find(id)
        if user:
            return user.json(), 200
        return {'message': 'User not found'}, 404

    @jwt_required()
    def delete(self, id):
        user = UserModel.user_find(id)
        if user:
            try:
                user.user_delete()
            except:
                return {'message': 'An internal error ocurred trying to save user'}, 500
            return {'message': 'User deleted'}, 204
        return {'message': 'User not found'}, 404

class UserRegister(Resource):
    def post(self):
        data = arguments.parse_args()
        if not data.get('email') or data.get('email') is None:
            return {'message':  'The field e-mail cannot be left blank'}, 400
        if UserModel.find_by_email(data['email']):
            return {'message': 'E-mail already exists'}, 400
        if UserModel.find_by_login(data['login']):
            return {'message': 'Login already exists'}, 400
        user = UserModel(**data)
        user.activate = False
        try:
            user.user_save()
            user.email_confirm()
            return {'message': 'User created successfully'}, 201
        except:
            user.user_delete()
            traceback.print_exc()
            return {'message': 'An internal error ocurred trying to save hotel'}, 500

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = arguments.parse_args()
        user = UserModel.find_by_login(data['login'])
        if user and safe_str_cmp(user.password, data['password']):
            if user.activate:
                token = create_access_token(identity=user.id)
                return {'access_token': token}, 200
            return {'message': 'User is not active'}, 400
        return {'message': 'Username or password is incorrect'}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        now = datetime.now(timezone.utc)
        logout = BlocklistModel.blocklist_add(jti, now)
        if logout:
            return {'message': 'Logged out successfully!'}, 200
        return {'message': 'Internal error server'}, 500
    
class UserActivate(Resource):
    @classmethod
    def get(cls, id):
        user = UserModel.user_find(id)
        if not user:
            return {'message': 'User not found'}, 404
        try:
            user.activate = True
            user.user_save()
            # return {'message': 'User activated successfully'}, 200
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('user_activate.html', email=user.email, user=user.name), 200, headers)
        except:
            return {'message': 'An internal error server occurred'}, 500

