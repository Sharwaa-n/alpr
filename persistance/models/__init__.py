from os import stat
from typing import Text
from ..utils.DB import db, Model
from ..utils.DB import ForeignKeyField, TextField, DateTimeField, PasswordField, CharField, BooleanField, IntegerField, datetime
from peewee_validates import ModelValidator
# __all__ = ['User', 'DetectionRequest', 'BaseModel']

class Val:
    errors = None
    def Validate(self):
        validator = ModelValidator(self)
        if validator.validate():
            return True
        else:
            self.errors = validator.errors
            return False
        
class BaseModel(Model, Val):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = PasswordField()
    active = BooleanField(default=False)
    api_token = TextField()
    token_recycled_date = DateTimeField()
    activated_date = DateTimeField()
    
    @property
    def serialize(self):
        data = {
            'id': self.id,
            'username': self.username,
            'active': self.active,
            'api_token': self.api_token,
            'token_recycled_date': self.token_recycled_date,
            'activated_date': self.activated_date,
        }
        return data

class DetectionRequest(BaseModel):
    image = TextField()
    user = ForeignKeyField(User, backref='submissions')
    created_date = DateTimeField(default=datetime.datetime.now)
    ip = TextField()

    @property
    def serialize(self):
        data = {
            'id': self.id,
            'image': self.image,
            'user': self.user.serialize,
            'created_date': self.created_date,
            'ip': self.ip,
        }
        return data

class Plate(BaseModel):
    number = TextField()
    remarks = TextField()
    last_detection_date = DateTimeField(default=datetime.datetime.now)

    @property
    def serialize(self):
        data = {
            'id': self.id,
            'number': self.number,
            'last_detection_date': self.last_detection_date,
        }
        return data

class Detection(BaseModel):
    request = ForeignKeyField(DetectionRequest, backref='detections')
    plate = ForeignKeyField(Plate, backref='plate_detections')
    created_date = DateTimeField(default=datetime.datetime.now)
    ip = TextField()
    verified = BooleanField(default=False)


    @property
    def serialize(self):
        data = {
            'id': self.id,
            'plate': self.plate.serialize,
            'request': self.request.serialize,
            'created_date': self.created_date,
            'ip': self.ip,
        }
        return data

class LostClaim(BaseModel):
    plate = ForeignKeyField(Plate, backref='claims')
    state = IntegerField(default=1) # 1 - Missing, 2 - Found, 3 - 
    remarks = TextField(null=True)
    created_date = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref='user_claims')

    @property
    def serialize(self):
        states = ['Missing', 'Found']
        data = {
            'id': self.id,
            'state': self.state,
            'stateName': states[self.state - 1],
            'plate': self.plate.serialize,
            'created_date': self.created_date,
            'user': self.user.serialize,
            'remarks': self.remarks
        }
        return data