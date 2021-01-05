from db import db


class DataModel(db.Model):
    __tablename__='data'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(20))
    speed = db.Column(db.Integer)
    uid = db.Column(db.Integer)

    def __init__(self, action, speed, uid):
        self.action = action
        self.speed = speed
        self.uid = uid

    def json(self):
        return{
            'id':self.id,
            'action': self.action,
            'speed': self.speed,
            'uid': self.uid
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    #not implemented as resource
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_uid(cls, uid):
        return cls.query.filter_by(uid=uid)