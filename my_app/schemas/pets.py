from marshmallow import Schema, fields

class PetSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    age = fields.String(required=True)
    sex = fields.String(required=True)
    specie = fields.String(required=True)
    owner_id = fields.String(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S.%f", required=True)