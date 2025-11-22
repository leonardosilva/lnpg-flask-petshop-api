from marshmallow import Schema, fields

class LoginSchema(Schema):
    email = fields.String(
        required=True, 
        metadata={
            "description":"Email de acesso"
        }
    )
    password = fields.String(
        required=True,
        metadata={
            "description":"Senha de acesso"
        }
    )

class LoginResponseSchema(Schema):
    access_token = fields.String(
        required=True,
        metadata={"description": "Token JWT para acesso às rotas protegidas"}
        )
    refresh_token = fields.String(
        required=True,
        metadata={"description": "Token para renovar o acesso expirado"}
        )

class LoginResponseFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    point = fields.String(
        required=True,
        metadata={
            "example": "login"
        }
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "Credenciais de acesso incorretas"
            }
        )
    
class RefreshSchema(Schema):
    access_token = fields.String(
        required=True,
        metadata={"description": "Token JWT para acesso às rotas protegidas"}
    )

class RefreshResponseFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={
            "example": False
        }
    )
    point = fields.String(
        required=True,
        metadata={
            "example": "renew_token"
        }
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "Sessão expirada. Faça login novamente."
            }
        )

