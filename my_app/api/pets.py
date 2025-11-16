from flask import Blueprint, jsonify, request
from ..services.pets import Pets  
from ..utils.validate import schemaValidate

pets_bp = Blueprint('pets', __name__)  

@pets_bp.route('/', methods=['GET'])
def get_pets():
    pets = Pets()
    filters = request.args.to_dict()

    pets = Pets() 
    data = []
    
    if not filters:
        data = pets.list()
    else:
        data = pets.search(filters)
        
    return jsonify({
        "success": True,
        "data": data
    }), 200

@pets_bp.route('/<int:pet_id>', methods=['GET'])
def get_pet_by_id(pet_id):
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

@pets_bp.route('/', methods=['POST'])
def create_pet():
    data = request.json
    
    # 1. Valida se os campos obrigatórios existem
    validation_error = schemaValidate(["name", "specie", "sex", "owner_id", "age"], data)
    
    if validation_error:
        return validation_error
        
    # 2. Valida a regra de negócio específica para o campo 'sex'
    sex = data.get("sex")
    if sex and sex.upper() not in ('M', 'F'):
        return jsonify({
            "success": False,
            "point": "create_pet_validation",
            "message": "O campo 'sex' deve ser 'M' (Macho) ou 'F' (Fêmea)."
        }), 400

    # 3. PADRONIZAÇÃO 
    # Se 'sex' foi enviado, atualiza o 'data' para a versão maiúscula
    if sex:
        data["sex"] = sex.upper()

    # 4. Se tudo estiver certo, continua com a criação
    pets = Pets()
    pets.create(data) 
    
    return jsonify({ "success": True }), 201

@pets_bp.route('/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    pets = Pets()
    try:
        pets.delete(pet_id)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "delete_pet",
            "message": str(err)
        }), 400
        
    return jsonify({ "success": True }), 200

@pets_bp.route('/<int:pet_id>', methods=['PATCH'])
def update_pet(pet_id):
    data = request.json
    
    # 1. Validação do schema original (campos proibidos no update)
    validation_error = schemaValidate(["id", "created_at"], data, False)
    
    if validation_error:
        return validation_error

    # 2. Nova validação: Regra de negócio para 'sex', 
    #    apenas se o campo 'sex' for enviado no JSON
    if "sex" in data:
        sex = data.get("sex")
        # Verifica se o valor não é nulo e se é diferente de 'M' ou 'F'
        if sex and sex.upper() not in ('M', 'F'):
            return jsonify({
                "success": False,
                "point": "update_pet_validation",
                "message": "O campo 'sex' deve ser 'M' (Macho) ou 'F' (Fêmea)."
            }), 400

        # Atualiza o 'data' para a versão maiúscula
        if sex:
            data["sex"] = sex.upper()
        # Se 'sex' for enviado como null ou "", 'data["sex"]' será null ou ""

    # 3. Se tudo estiver certo, continua com o update
    pets = Pets()
    try:
        pets.update(pet_id, data)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "update_pet",
            "message": str(err)
        }), 400
        
    return jsonify({ "success": True }), 200