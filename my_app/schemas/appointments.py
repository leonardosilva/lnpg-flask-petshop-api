from marshmallow import Schema, fields, validate
from .pets import PetSchema
from .employee import EmployeeSchema
from .service import ServiceSchema

class AppointmentSchema(Schema):
    id = fields.String(required=True)
    status = fields.String(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S.%f",  required=True)
    scheduled_at = fields.DateTime(format="iso",  required=True)
    employee = fields.Nested(EmployeeSchema, required=True)
    pet = fields.Nested(PetSchema, required=True)
    service = fields.Nested(ServiceSchema, required=True)

class GetAppointmentResponseSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": True
        }
    )
    data = fields.List(
        fields.Nested(AppointmentSchema), 
        required=True,
        metadata={
            "description": "Lista de agendamentos",
            "example": [
                    {
                        "created_at": "2025-11-15 23:04:52.890929",
                        "employee": {
                            "created_at": "2025-11-19 19:01:57.357203",
                            "email": "leo@ifal.edu.br",
                            "id": "1",
                            "job_title": "Veterinário",
                            "name": "LEONARDO",
                        },
                        "id": "3",
                        "pet": {
                            "age": "30",
                            "created_at": "2025-11-10 22:13:45.951335",
                            "id": "1",
                            "name": "Abel",
                            "owner_id": "1",
                            "sex": "F",
                            "specie": "cat"
                        },
                        "scheduled_at": "2025-11-16T13:39:57.228996",
                        "service": None,
                        "status": "finished"
                }
            ]
        }
    )

class GetAppointmentsByIDResponseSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": True
        }
    )
    data = fields.Nested(
        AppointmentSchema, 
        required=True,
        metadata={
            "description": "Agendamento encontrado com base no ID informado",
            "example":  {
                    "created_at": "2025-11-15 23:04:52.890929",
                    "employee": {
                        "created_at": "2025-11-19 19:01:57.357203",
                        "email": "leo@ifal.edu.br",
                        "id": "1",
                        "job_title": "Veterinário",
                        "name": "LEONARDO",
                    },
                    "id": "3",
                    "pet": {
                        "age": "30",
                        "created_at": "2025-11-10 22:13:45.951335",
                        "id": "1",
                        "name": "Abel",
                        "owner_id": "1",
                        "sex": "F",
                        "specie": "cat"
                    },
                    "scheduled_at": "2025-11-16T13:39:57.228996",
                    "service": None,
                    "status": "finished"
            }
        }
    )

class GetAppointmentsByIDResponseNoutFoundSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    point = fields.String(
        required=True,
        metadata={
            "example": "get_appointment_by_id"
        }
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "Agendamento não encontrado"
            }
        )
    
class CreateAppointmentSchema(Schema):
    pet_id = fields.Integer(
        required=True,
        metadata={
            "description": "ID do Pet que será atendido.",
            "example": 1
        }
    )
    service_id = fields.Integer(
        required=True,
        metadata={
            "description": "ID do Serviço a ser realizado.",
            "example": 1
        }
    )
    employee_id = fields.Integer(
        required=True,
        metadata={
            "description": "ID do Funcionário responsável pelo atendimento.",
            "example": 1
        }
    )
    scheduled_at = fields.DateTime(
        required=True,
        format="iso",
        metadata={
            "description": "Data e hora programada para o agendamento (formato ISO 8601).",
            "example": "2025-12-18T10:36:13.226"
        }
    )

class CreateAppointmentResponseFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    point = fields.String(
        required=True,
        metadata={
            "example": "create_appointment"
        }
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "Pet não encontrado"
            }
        )
    
class DeleteAppointmentResponseFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    point = fields.String(
        required=True,
        metadata={
            "example": "delete_appointment"
        }
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "ID não existe"
            }
        )
    
class UpdateAppointmentResponseFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    point = fields.String(
        required=True,
        metadata={
            "example": "update_appointment"
        }
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "ID não existe"
            }
        )
    
class UpdateAppointmentSchema(Schema):
    pet_id = fields.Integer(
        required=False,
        metadata={
            "description": "ID do Pet que será atendido.",
            "example": 1
        }
    )
    service_id = fields.Integer(
        required=False,
        metadata={
            "description": "ID do Serviço a ser realizado.",
            "example": 1
        }
    )
    employee_id = fields.Integer(
        required=False,
        metadata={
            "description": "ID do Funcionário responsável pelo atendimento.",
            "example": 1
        }
    )
    scheduled_at = fields.DateTime(
        required=False,
        format="iso",
        metadata={
            "description": "Data e hora programada para o agendamento (formato ISO 8601).",
            "example": "2025-12-18T10:36:13.226"
        }
    )
    status = fields.String(
        required=False,
        validate=validate.OneOf(["scheduled", "finished", "canceled"]),
        metadata={
            "description": "Status do agendamento. Valores permitidos: 'scheduled', 'finished', 'canceled'.",
            "example": "finished"
        }
    )
