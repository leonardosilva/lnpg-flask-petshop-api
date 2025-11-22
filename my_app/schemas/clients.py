from marshmallow import Schema, fields
from .pets import PetSchema

class ClientSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S.%f", required=True)
    pets = fields.List(fields.Nested(PetSchema), required=True)

class GetClientsResponseSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": True
        }
    )
    data = fields.List(
        fields.Nested(ClientSchema), 
        required=True,
        metadata={
            "description": "Lista de clientes e seus pets",
            "example": [
                {
                    "created_at": "2025-11-15 14:36:43.122189",
                    "email": "mvbs16@aluno.ifal.edu.br",
                    "id": "2",
                    "name": "MARCOS VINICIUS BEZERRA SILVA",
                    "pets": [
                        {
                            "age": "90",
                            "created_at": "2025-11-10 23:00:19.958425",
                            "id": "2",
                            "name": "Biruta",
                            "owner_id": "2",
                            "sex": "F",
                            "specie": "cat"
                        }
                    ],
                    "phone": "82987130427"
                }
            ]
        }
    )

class GetClientsByIDResponseSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": True
        }
    )
    data = fields.Nested(
        ClientSchema, 
        required=True,
        metadata={
            "description": "Cliente encontrado com base no ID informado",
            "example": {
                "created_at": "2025-11-15 14:36:43.122189",
                "email": "mvbs16@aluno.ifal.edu.br",
                "id": "2",
                "name": "MARCOS VINICIUS BEZERRA SILVA",
                "pets": [
                    {
                        "age": "90",
                        "created_at": "2025-11-10 23:00:19.958425",
                        "id": "2",
                        "name": "Biruta",
                        "owner_id": "2",
                        "sex": "F",
                        "specie": "cat"
                    }
                ],
                "phone": "82987130427"
            }
        }
    )

class GetClientsByIDResponseNoutFoundSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    point = fields.String(
        required=True,
        metadata={
            "example": "get_client_by_id"
        }
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "Cliente não encontrado"
            }
        )
    
class CreateClientSchema(Schema):
    name = fields.String(
        required=True,
        metadata={
            "description": "Nome completo do cliente.",
            "example": "Teste 1"
        }
    )
    email = fields.String(
        required=True,
        metadata={
            "description": "Email de contato do cliente (deve ser único).",
            "example": "mvbs15@aluno.ifal.edu.br"
        }
    )
    phone = fields.String(
        required=True,
        metadata={
            "description": "Número de telefone do cliente.",
            "example": "82987130427"
        }
    )


class CreateClientResponseFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    point = fields.String(
        required=True,
        metadata={
            "example": "create_client"
        }
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "O e-mail informado já está em uso"
            }
        )

class DeleteClientResponseFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    point = fields.String(
        required=True,
        metadata={
            "example": "delete_client"
        }
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "ID não existe"
            }
        )
    
class UpdateClientResponseFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    point = fields.String(
        required=True,
        metadata={
            "example": "update_client"
        }
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "ID não existe"
            }
        )
    
class UpdateClientSchema(Schema):
    name = fields.String(
        required=False,
        metadata={
            "description": "Nome completo do cliente.",
            "example": "Teste 1"
        }
    )
    email = fields.String(
        required=False,
        metadata={
            "description": "Email de contato do cliente (deve ser único).",
            "example": "mvbs15@aluno.ifal.edu.br"
        }
    )
    phone = fields.String(
        required=False,
        metadata={
            "description": "Número de telefone do cliente.",
            "example": "82987130427"
        }
    )

