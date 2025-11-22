from marshmallow import Schema, fields

class GenericSuccessSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": True
        }
    )