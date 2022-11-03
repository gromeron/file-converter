from flask_sqlalchemy import SQLAlchemy
import enum
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()

class Status(enum.Enum):
    UPLOADED = 1
    PROCESSED = 2

class FileFormat(enum.Enum):
    MP3 = 1
    OGG = 2
    WAV = 3
    ACC = 4
    WMA = 5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    #tasks = db.relationship('User', cascade='all, delete, delete-orphan')


    # Testing console output
    """ def __repr__(self):
        return '{} - {} - {}'.format(self.username, self.email, self.password) """

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #timestamp = db.Column(db.Datetime, default=datetime.utcnow)
    status = db.Column(db.Enum(Status))
    originalFormat = db.Column(db.Enum(FileFormat))
    newFormat = db.Column(db.Enum(FileFormat))
    #user = db.relationship('User', backref='task')
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Serializing
# Enumeration table
class EnumADcicionario(fields.Field):
    # Method from class
    def _serialize(self, value, attr, obj, *kwargs):
        # Not serialize empty fields
        if value is None:
            return None
        # Return enum name and value
        return {'llave':value.name, 'valor':value.value}


# User
class UserSchema(SQLAlchemyAutoSchema):
    class meta:
        model = User
        include_relationships = True
        load_instance = True

    username = fields.String()
    email = fields.String()
    password = fields.String()
    #tasks = fields.List(fields.Nested(TaskSchema()))

# Task
class TaskSchema(SQLAlchemyAutoSchema):
    status = EnumADcicionario(attribute=('status'))
    originalFormat = EnumADcicionario(attribute=('fileFormat'))
    newFormat = EnumADcicionario(attribute=('fileFormat'))
    class meta:
        model = Task
        include_relationship = True
        load_instance = True

    status = fields.String()
    originalFormat = fields.String()
    newFormat = fields.String()
    #user = fields.List(fields.Nested(UserSchema()))