from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.hotels import Hotels, Hotel, HotelRegister
from resources.sites import Sites, Site, SiteRegister
from resources.users import User, UserRegister, UserLogin, UserLogout, UserActivate
from datetime import timedelta
from sql_alchemy import banco
from models.blocklist import BlocklistModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask:flask@172.17.0.2/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
ACCESS_EXPIRES = timedelta(hours=12)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    return '<h1> Hello</h1>'

@app.before_first_request
def create_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = BlocklistModel.token_filter(jti)
    return token is not None

api.add_resource(Hotels, '/hotels')
api.add_resource(Hotel, '/hotels/<int:id>')
api.add_resource(HotelRegister, '/hotels/register')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<int:id>')
api.add_resource(SiteRegister, '/sites/register')
api.add_resource(User, '/users/<int:id>')
api.add_resource(UserRegister, '/users/register')
api.add_resource(UserActivate, '/users/activate/<int:id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=80)