from flask import jsonify, request
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from ..services.pets import Pets
from ..utils.validate import schemaValidate, ValidationFailedSchema

# Importando Schemas 
from ..schemas.pets import (
    GetPetsResponseSchema,
    GetPetsByIDResponseSchema,
    GetPetsByIDResponseNotFoundSchema,
    CreatePetSchema,
    CreatePetResponseFailedSchema,
    DeletePetResponseFailedSchema,
    UpdatePetResponseFailedSchema,
    UpdatePetSchema
)
from ..schemas.generic import GenericSuccessSchema

pets_bp = Blueprint('pets', __name__)

# -----------------------------------------------------------------------------
# ROTA: LISTAR PETS
# -----------------------------------------------------------------------------
@pets_bp.route('/', methods=['GET'])
@pets_bp.response(200, GetPetsResponseSchema, description="Listar pets")
@pets_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_pets():
    """Buscar lista de pets

    Retorna a lista de todos os pets cadastrados na plataforma.
    É possível realizar filtros na hora de realizar a busca (ex: name, specie).
    """
    pets = Pets()
    filters = request.args.to_dict()
    data = []

    if not filters:
        data = pets.list()
    else:
        data = pets.search(filters)

    return jsonify({
        "success": True,
        "data": data
    }), 200

# -----------------------------------------------------------------------------
# ROTA: BUSCAR PET POR ID
# -----------------------------------------------------------------------------
@pets_bp.route('/<int:pet_id>', methods=['GET'])
@pets_bp.response(200, GetPetsByIDResponseSchema, description="Pet encontrado")
@pets_bp.response(404, GetPetsByIDResponseNotFoundSchema, description="Pet não encontrado")
@pets_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_pet_by_id(pet_id):
    """Buscar pet pelo ID
    
    Faz a busca de um pet pelo ID e retorna erro se não encontrar.
    """
    pets = Pets()
    pet = pets.get_by_id(pet_id)

    if pet:
        return jsonify({
            "success": True,
            "data": pet
        }), 200

    return jsonify({
        "success": False,
        "point": "get_pet_by_id",
        "message": "Pet não encontrado"
    }), 404

# -----------------------------------------------------------------------------
# ROTA: CRIAR PET
# -----------------------------------------------------------------------------
@pets_bp.route('/', methods=['POST'])
@pets_bp.doc(security=[{"bearerAuth": []}])
@pets_bp.doc(
    requestBody={
        "content": {
            "application/json": {
                "schema": CreatePetSchema,
                "required": True
            }
        }
    }
)
@pets_bp.response(422, ValidationFailedSchema, description="Falha na validação dos campos")
@pets_bp.response(400, CreatePetResponseFailedSchema, description="Falha ao criar o pet.")
@pets_bp.response(201, GenericSuccessSchema, description="Pet criado com sucesso")
@jwt_required()
def create_pet():
    """Criar novo pet"""
    data = request.json
    
    # 1. Validação genérica (existência dos campos)
    validation_error = schemaValidate(["name", "specie", "sex", "owner_id", "age"], data)
    if validation_error:
        return validation_error

    # 2. Validação Específica de Regra de Negócio (Sexo)
    sex = data.get("sex")
    if sex and sex.upper() not in ('M', 'F'):
        return jsonify({
            "success": False,
            "point": "create_pet_validation",
            "message": "O campo 'sex' deve ser 'M' (Macho) ou 'F' (Fêmea)."
        }), 400
    
    # Padronização
    if sex:
        data["sex"] = sex.upper()

    pets = Pets()
    try:
        pets.create(data)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "create_pet",
            "message": str(err)
        }), 400

    return jsonify({"success": True}), 201

# -----------------------------------------------------------------------------
# ROTA: DELETAR PET
# -----------------------------------------------------------------------------
@pets_bp.route('/<int:pet_id>', methods=['DELETE'])
@pets_bp.doc(security=[{"bearerAuth": []}])
@pets_bp.response(200, GenericSuccessSchema, description="Pet deletado com sucesso")
@pets_bp.response(400, DeletePetResponseFailedSchema, description="Pet não encontrado")
@jwt_required()
def delete_pet(pet_id):
    """Deletar pet"""
    pets = Pets()
    try:
        pets.delete(pet_id)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "delete_pet",
            "message": str(err)
        }), 400

    return jsonify({"success": True}), 200

# -----------------------------------------------------------------------------
# ROTA: ATUALIZAR PET
# -----------------------------------------------------------------------------
@pets_bp.route('/<int:pet_id>', methods=['PATCH'])
@pets_bp.doc(security=[{"bearerAuth": []}])
@pets_bp.doc(
    requestBody={
        "content": {
            "application/json": {
                "schema": UpdatePetSchema,
                "required": False
            }
        }
    }
)
@pets_bp.response(422, ValidationFailedSchema, description="Falha na validação dos campos")
@pets_bp.response(400, UpdatePetResponseFailedSchema, description="Pet não encontrado")
@pets_bp.response(200, GenericSuccessSchema, description="Pet editado com sucesso")
@jwt_required()
def update_pet(pet_id):
    """Editar pet
    
    Todos os campos podem ser editados, exceto id e created_at.
    """
    data = request.json
    
    # 1. Validação genérica (impedir alteração de id/data)
    validation_error = schemaValidate(["id", "created_at"], data, False)
    if validation_error:
        return validation_error

    # 2. Validação Específica (Sexo)
    if "sex" in data:
        sex = data.get("sex")
        if sex and sex.upper() not in ('M', 'F'):
            return jsonify({
                "success": False,
                "point": "update_pet_validation",
                "message": "O campo 'sex' deve ser 'M' (Macho) ou 'F' (Fêmea)."
            }), 400
        if sex:
            data["sex"] = sex.upper()

    pets = Pets()
    try:
        pets.update(pet_id, data)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "update_pet",
            "message": str(err)
        }), 400

    return jsonify({"success": True}), 200