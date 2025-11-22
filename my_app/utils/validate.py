from typing import List, AnyStr
from flask import jsonify
from datetime import datetime as dt, date
from marshmallow import Schema, fields

def schemaValidate(list_fields: List[AnyStr], data: dict, missing = True):
    if missing:
        missing_fields = []
        for field in list_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
                
        if missing_fields:
            return jsonify({
                "success": False,
                "error": "Campos obrigatórios estão faltando ou estão vazios.",
                "missing": missing_fields
            }), 422 

        return None
    else:
        blocked_fields = []
        for field in list_fields:
            if field in data:
                blocked_fields.append(field)
                
        if blocked_fields:
            return jsonify({
                "success": False,
                "error": "Alguns campos informados estão bloqueados.",
                "blocked": blocked_fields
            }), 422 

        return None
    

def validateScheduledAt(date_string: str, date_format='%Y-%m-%dT%H:%M:%S.%f'):
        if not date_string:
            return False 
        
        actual_date = date.today()

        try:
            scheduled_dt = dt.strptime(date_string, date_format)
            scheduled_date = scheduled_dt.date()

            return scheduled_date >= actual_date
        except ValueError:
            return False
   

class ValidationFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    error = fields.String(
        required=True,
        metadata={
            "description": "Descrição do erro",
            "example": "Campos obrigatórios estão faltando ou estão vazios."
        }
    )
    missing = fields.List(
        fields.String(),
        required=False,
        metadata={
            "description": "Array com a lista de campos faltando",
            "example": ["email", "password"]
            }
        )
    blocked = fields.List(
        fields.String(),
        required=False,
        metadata={
            "description": "Array com a lista de campos bloqueados",
            "example": ["id", "created_at"]
            }
        )
