from marshmallow import fields
from app.models import Note
from app.extensions import ma


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True

    created_at = ma.DateTime(format="%Y-%m-%dT%H:%M:%S")


class UserSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
