from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt_claims,
    jwt_required
)
import RPi.GPIO as IO
import time
from models.data import DataModel
from robopi.action import Action
import global_var


action = Action()

data_parser = reqparse.RequestParser()
data_parser.add_argument('action',
                type = str,
                required = False,
                )
data_parser.add_argument('speed',
                type=int,
                required=False,
                )
data_parser.add_argument('latitude',
                type=float,
                required=False,
                )
data_parser.add_argument('longitude',
                type=float,
                required=False,
                )
data_parser.add_argument('angle',
                type=int,
                required=False,
                )
data_parser.add_argument('length',
                type=float,
                required=False,
                )
data_parser.add_argument('breadth',
                type=float,
                required=False,
                )
data_parser.add_argument('turn_speed',
                type=int,
                required=False,
                )
data_parser.add_argument('turn_angle',
                type=int,
                required=False,
                )

class Mobilize(Resource):
    # @jwt_required
    def post(self):
        # claims = get_jwt_claims()
        # if claims['is_admin']: #add jwt claims in future
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
    # return {'message': "Admin privilege Required!!!"}

class Proximity(Resource):
    # @jwt_required
    def get(self):
        proximity = action.proximity()
        return {"proximity": proximity}

class Position(Resource):
    def get(self):
        lat, longi = action.position()
        return {"latitude": lat, "longitude": longi}

class Bearing(Resource):
    def get(self):
        bearing = action.positionBearing()
        return {"bearing": bearing}
        

#not completed yet (don't call this method)
#returns all commands of a particular user
class Stat(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id):
        data = DataModel.find_by_uid(user_id).first()
        return data.json()

class Turn(Resource):
    def post(self):
        data = data_parser.parse_args()
        speed = data["speed"]
        turnangle = data["angle"]
        action.turn(turnangle, speed)
        currentangle = action.positionBearing()
        return {"turnangle": turnangle, "currentangle": currentangle, "speed": speed}

class Autonomous(Resource):
    def post(self):
        data = data_parser.parse_args()
        lat1, longi1 = action.position()
        lat2, longi2, speed = data["latitude"], data["longitude"], data["speed"]
        bposn = action.positionBearing()
        bdest = action.destinationBearing(lat1, longi1, lat2, longi2)
        initial_turnangle = action.turnAngle(bposn, bdest)
        turnangle = initial_turnangle
        action.turn(turnangle, speed)
        return { "latitude": latitude, "longitude": longitude, "turnangle": initial_turnangle}, 200

class Arm(Resource):
    def post(self):
        data = data_parser.parse_args()
        angle = data["angle"]
        action.arm(angle)
        return {"angle": angle}

class PseudoAuto(Resource):
    def post(self):
        data = data_parser.parse_args()
        length, breadth = data["length"], data["breadth"]
        forward_speed, turn_speed = data["speed"], data["turn_speed"]
        turn_angle = data["turn_angle"]

        arm_up = 60
        arm_down = 90
        itration_number = int(breadth) + 1
        length = int(length * 10)
        vehicle_width = 20
        global_var.i_length, global_var.i_breadth = 0, 0
        for i in range(itration_number):
            if i % 2 == 0:
                action.stop()
                action.arm(arm_down)
                action.auto_forward(forward_speed, length)

                action.stop()
                action.arm(arm_up)
                action.turn(turn_angle, turn_speed)

                action.stop()
                action.arm(arm_down)
                action.auto_forward_short(forward_speed, vehicle_width)

                action.stop()
                action.arm(arm_up)
                action.turn(turn_angle, turn_speed)
            else:    
                action.stop()
                action.arm(arm_down)
                action.auto_forward(forward_speed, length)

                action.stop()
                action.arm(arm_up)
                action.turn(-turn_angle, turn_speed)

                action.stop()
                action.arm(arm_down)
                action.auto_forward_short(forward_speed, vehicle_width)

                action.stop()
                action.arm(arm_up)
                action.turn(-turn_angle, turn_speed)

        return {"message": "success", "i_length": global_var.i_length, "i_breadth": global_var.i_breadth}

class PseudoLocation(Resource):
    def get(self):
        return {"i_length": global_var.i_length, "i_breadth":global_var.i_breadth}

class Terminate(Resource):
    def delete(self):
        IO.cleanup()