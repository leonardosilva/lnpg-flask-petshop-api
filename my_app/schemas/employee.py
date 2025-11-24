from marshmallow import Schema, fields

class EmployeeSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    job_title = fields.String(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S.%f")

class GetEmployeesResponseSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": True
        }
    )
    data = fields.List(
        fields.Nested(EmployeeSchema), 
        required=True,
        metadata={
            "description": "Lista de funcionários",
            "example": [
                {
                    "created_at": "2025-11-19 19:01:57.357203",
                    "email": "leo@ifal.edu.br",
                    "id": "1",
                    "job_title": "Veterinário",
                    "name": "LEONARDO"
                }
            ],
        }
    )

class GetEmployeesByIDResponseSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": True
        }
    )
    data = fields.Nested(
        EmployeeSchema, 
        required=True,
        metadata={
            "description": "Funcionário encontrado com base no ID informado",
            "example": {
                "created_at": "2025-11-19 19:01:57.357203",
                "email": "leo@ifal.edu.br",
                "id": "1",
                "job_title": "Veterinário",
                "name": "LEONARDO"
            }
        }
    )


class GetEmployeesByIDResponseNoutFoundSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    point = fields.String(
        required=True,
        metadata={
            "example": "get_employee_by_id"
        }
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "Funcionário não encontrado"
            }
        )
  
