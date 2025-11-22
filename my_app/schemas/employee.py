from marshmallow import Schema, fields

class EmployeeSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    job_title = fields.String(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S.%f")