from flask import  jsonify, request
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from ..services.clients import Clients
from ..utils.validate import schemaValidate, ValidationFailedSchema
from ..schemas.clients import GetClientsResponseSchema, GetClientsByIDResponseSchema, GetClientsByIDResponseNoutFoundSchema, CreateClientSchema, CreateClientResponseFailedSchema, DeleteClientResponseFailedSchema, UpdateClientResponseFailedSchema, UpdateClientSchema
from ..schemas.generic import GenericSuccessSchema

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/', methods=['GET'])
@clients_bp.response(200, GetClientsResponseSchema, description="Listar clientes")
@clients_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_clients():
    """Buscar lista de clientes

        Retorna a lista de todos os clientes cadastrados na plataforma.
        É possível realizar filtros na hora de realizar a busca. Abaixo estão os filtros válidos:
        * `logic` - Usado para dizer qual tipo de operador lógico utilizar para comparação. Valores válidos: `AND` e `OR`.O valor padrão é `AND`.
        * `operator` - Usado para informar que tipo de comparação deve ser feita. Valores válidos: ,`EQUAL`,`NOT_EQUAL`,`CONTAINS`,`LESS_THAN`,`MORE_THAN`,`LESS_THAN_OR_EQUAL`,`MORE_THAN_OR_EQUAL`O valor padrão é ,`CONTAINS`
        * `name` - Nome do cliente.
        * `phone` - Telefone do cliente.
        * `email` - Email do cliente.
    """
    clients = Clients()
    filters = request.args.to_dict()
    
    clients = Clients()
    data = []

    if not filters:
        data = clients.list()
    else:
        data = clients.search(filters)

    return jsonify({
        "success": True,
        "data": data
    }), 200

@clients_bp.route('/<int:client_id>', methods=['GET'])
@clients_bp.response(200, GetClientsByIDResponseSchema, description="Cliente encontrado")
@clients_bp.response(404, GetClientsByIDResponseNoutFoundSchema, description="Cliente não encontrado")
@clients_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_client_by_id(client_id):
    """Buscar cliente pelo ID

        Faz a busca de um cliente pelo ID e retorna erro se não encontrar.
    """
    clients = Clients()
    client = clients.get_by_id(client_id)
    if client: 
        return jsonify({
            "success": True,
            "data": client
        }), 200
    
    return jsonify({
        "success": False,
        "point": "get_client_by_id",
        "message": "Cliente não encontrado"
    }), 404


@clients_bp.route('/', methods=['POST'])
@clients_bp.doc(security=[{"bearerAuth": []}])
@clients_bp.doc(
    requestBody={
        "content": {
            "application/json": {
                "schema": CreateClientSchema 
            }
        },
        "required": True 
    }
)
@clients_bp.response(422, ValidationFailedSchema, description="Falha na validação dos campos")
@clients_bp.response(400, CreateClientResponseFailedSchema, description="Falha ao criar o cliente.")
@clients_bp.response(201, GenericSuccessSchema, description="Cliente criado com sucesso")
@jwt_required()
def create_client():
    """Criar novo cliente
    """
    data = request.json

    validation_error = schemaValidate(["name", "phone", "email"], data)

    if validation_error:
        return validation_error
    
    clients = Clients()
    try:
        clients.create(data)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "create_client",
            "message": str(err)
        }), 400
    

    return jsonify({ "success": True }), 201

@clients_bp.route('/<int:client_id>', methods=['DELETE'])
@clients_bp.doc(security=[{"bearerAuth": []}])
@clients_bp.response(200, GenericSuccessSchema, description="Cliente deletado com sucesso")
@clients_bp.response(400, DeleteClientResponseFailedSchema, description="Cliente não encontrado")
@jwt_required()
def delete_client(client_id):
    """Deletar cliente
    """
    clients = Clients()
    try:
        clients.delete(client_id)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "delete_client",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

@clients_bp.route('/<int:client_id>', methods=['PATCH'])
@clients_bp.doc(security=[{"bearerAuth": []}])
@clients_bp.doc(
    requestBody={
        "content": {
            "application/json": {
                "schema": UpdateClientSchema 
            }
        },
        "required": False 
    }
)
@clients_bp.response(422, ValidationFailedSchema, description="Falha na validação dos campos")
@clients_bp.response(400, UpdateClientResponseFailedSchema, description="Cliente não encontrado")
@clients_bp.response(200, GenericSuccessSchema, description="Cliente editado com sucesso")
@jwt_required()
def update_client(client_id):
    """Editar cliente

    Todos os campos do cliente podem ser editados. Exceto: 
    * id
    * created_at
    """
    data = request.json
    validation_error = schemaValidate(["id", "created_at"], data, False)

    if validation_error:
        return validation_error
    
    clients = Clients()
    try:
        clients.update(client_id, data)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "update_client",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

        