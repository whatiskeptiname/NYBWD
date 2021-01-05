from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt_claims,
    jwt_required
)
from models.data import DataModel
from robopi.action import Action

action = Action()


data_parser = reqparse.RequestParser()
data_parser.add_argument('action',
                type = str,
                required = True,
                help="This field can not be blank!!!"
                )
data_parser.add_argument('speed',
                type=int,
                required=True,
                help="This field can not be blank!!!"
                )


class Mobilize(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if claims['is_admin']:
            data = data_parser.parse_args()
            uid = get_jwt_identity();
            datamodel = DataModel(data['action'], data['speed'], uid)
            datamodel.save_to_db()

            if data['action'] == "left":
                action.left(data["speed"])
            elif data['action'] == "forward":
                action.forward(data["speed"])
            elif data['action'] == "right":
                action.right(data["speed"])
            elif data['action'] == "backward":
                action.backward(data["speed"])
            elif data['action'] == "stop":
                action.stop()
            return datamodel.json()
        return {'message': "Admin privilege Required!!!"}


#not completed yet (don't call this method)
#returns all commands of a particular user
class Stat(Resource):
    @classmethod
    # @jwt_required
    def get(cls, user_id):
        data = DataModel.find_by_uid(user_id).first()
        return data.json()