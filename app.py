from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh, ME
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'notNYBWD'
api = Api(app)

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


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(ME, '/me')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port =9000, debug=True)