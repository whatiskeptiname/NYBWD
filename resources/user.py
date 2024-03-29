from flask_restful import Resource, reqparse
from flask import render_template, make_response
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import(
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help = "This field can't be blank."
                    )
_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field can't be blank."
                    )

class Home(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "Username already taken!"}, 409

        user = UserModel(data['username'], data['password'])
        user.save_to_db()
        return{"message": "User created successfully."}, 201

class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "user not found!!!"}
        return user.json()

    @classmethod
    @jwt_required
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "user not found!!!"}
        user.delete_from_db()
        return {'message': "User deleted!!!"}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                'access_token': access_token,
                'refresh_token': refresh_token,
                'message': "User logged in sucessfully."
            }, 200
        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] #jti is 'JWt ID , a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {'message': "User logged out successfully!!!"}, 200

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

class ME(Resource):
    @jwt_required
    def get(self):
        return { 'user_id': get_jwt_identity()}