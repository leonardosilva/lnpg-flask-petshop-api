from marshmallow import Schema, fields

class ServiceSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    value = fields.Float(required=True)
    description = fields.String(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S.%f", required=True)

