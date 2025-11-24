from marshmallow import Schema, fields

# -----------------------------------------------------------------------------
# SCHEMA PRINCIPAL 
# -----------------------------------------------------------------------------
class PetSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    specie = fields.String(required=True)
    sex = fields.String(required=True)
    age = fields.Integer(required=True)
    owner_id = fields.Dict(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S.%f", required=True)

# -----------------------------------------------------------------------------
# SCHEMAS DE RESPOSTA (GET)
# -----------------------------------------------------------------------------
class GetPetsResponseSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={"example": True}
    )
    data = fields.List(
        fields.Nested(PetSchema),
        required=True,
        metadata={
            "description": "Lista de pets cadastrados",
            "example": [{
                "id": "1",
                "name": "Bolinha",
                "specie": "Cachorro",
                "sex": "M",
                "age": 3,
                "owner_id": "2",
                "created_at": "2025-11-15 14:36:43.122189"
            }]
        }
    )

class GetPetsByIDResponseSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={"example": True}
    )
    data = fields.Nested(
        PetSchema,
        required=True,
        metadata={
            "description": "Pet encontrado com base no ID informado",
            "example": {
                "id": "1",
                "name": "Bolinha",
                "specie": "Cachorro",
                "sex": "M",
                "age": 3,
                "owner_id": "2",
                "created_at": "2025-11-15 14:36:43.122189"
            }
        }
    )

class GetPetsByIDResponseNotFoundSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={"example": False}
    )
    point = fields.String(
        required=True,
        metadata={"example": "get_pet_by_id"}
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "Pet não encontrado"
        }
    )

# -----------------------------------------------------------------------------
# SCHEMAS DE CRIAÇÃO (POST)
# -----------------------------------------------------------------------------
class CreatePetSchema(Schema):
    name = fields.String(
        required=True,
        metadata={"description": "Nome do pet.", "example": "Rex"}
    )
    specie = fields.String(
        required=True,
        metadata={"description": "Espécie do pet (ex: Cachorro, Gato).", "example": "Cachorro"}
    )
    sex = fields.String(
        required=True,
        metadata={"description": "Sexo do pet (M ou F).", "example": "M"}
    )
    age = fields.Integer(
        required=True,
        metadata={"description": "Idade do pet em anos.", "example": 5}
    )
    owner_id = fields.Integer(
        required=True,
        metadata={"description": "ID do dono (Client) ao qual o pet pertence.", "example": 1}
    )

class CreatePetResponseFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={"example": False}
    )
    point = fields.String(
        required=True,
        metadata={"example": "create_pet"}
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "Erro ao criar pet"
        }
    )

# -----------------------------------------------------------------------------
# SCHEMAS DE DELEÇÃO (DELETE)
# -----------------------------------------------------------------------------
class DeletePetResponseFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={"example": False}
    )
    point = fields.String(
        required=True,
        metadata={"example": "delete_pet"}
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "ID não existe"
        }
    )

# -----------------------------------------------------------------------------
# SCHEMAS DE ATUALIZAÇÃO (PATCH)
# -----------------------------------------------------------------------------
class UpdatePetSchema(Schema):
    name = fields.String(
        required=False,
        metadata={"description": "Nome do pet.", "example": "Rex Silva"}
    )
    specie = fields.String(
        required=False,
        metadata={"description": "Espécie do pet.", "example": "Cachorro"}
    )
    sex = fields.String(
        required=False,
        metadata={"description": "Sexo do pet (M ou F).", "example": "M"}
    )
    age = fields.Integer(
        required=False,
        metadata={"description": "Idade do pet.", "example": 6}
    )
    # owner_id geralmente não se altera no update simples, mas pode ser adicionado se necessário

class UpdatePetResponseFailedSchema(Schema):
    success = fields.Boolean(
        required=True,
        metadata={"example": False}
    )
    point = fields.String(
        required=True,
        metadata={"example": "update_pet"}
    )
    message = fields.String(
        required=True,
        metadata={
            "description": "Mensagem de erro",
            "example": "ID não existe"
        }
    )