from flask import Flask, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh, ME, Home
from resources.mobilize import (
    Mobilize,
    Stat,
    Proximity,
    Position,
    Bearing,
    Autonomous,
    Arm,
    Turn,
    Terminate,
    PseudoAuto,
    PseudoLocation
)
from blacklist import BLACKLIST

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['CORS_HEADERS'] = 'application/json'
app.secret_key = 'notNYBWD'
api = Api(app)
CORS(app)
DebugToolbarExtension(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description':"The token has expired!!!",
        'error': "token_expired"
    }), 401

@jwt.invalid_token_loader
def  invalid_tokencallback(error):
    return jsonify({
        'description': "Signature varification failed!!!",
        'error': "invalid_token"
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': "Request does not contain an access token",
        'error': "authorization_required"
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': "The token is not fresh.",
        'error': "fresh_token_required"
    }), 401

api.add_resource(Home, '/')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(ME, '/me')
api.add_resource(Mobilize, '/mobilize')
api.add_resource(Proximity, '/proximity')
api.add_resource(Position, '/position')
api.add_resource(Bearing, '/bearing')
api.add_resource(Autonomous, '/autonomous')
api.add_resource(PseudoAuto, '/pseudoauto')
api.add_resource(PseudoLocation, '/pseudolocation')
api.add_resource(Turn, '/turn')
api.add_resource(Arm, '/arm')
api.add_resource(Terminate, '/terminate')
api.add_resource(Stat, '/stat/<int:user_id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0',port =9000, debug=True)