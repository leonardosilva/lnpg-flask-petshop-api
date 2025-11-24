from flask import  jsonify, request
from flask_smorest import Blueprint
from ..services.employees import Employees
from ..utils.validate import schemaValidate
from ..schemas.employee import GetEmployeesResponseSchema, GetEmployeesByIDResponseNoutFoundSchema, GetEmployeesByIDResponseSchema
from flask_jwt_extended import jwt_required

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/', methods=['GET'])
@employees_bp.response(200, GetEmployeesResponseSchema, description="Listar funcionários")
@employees_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_employees():
    """Buscar lista de funcionários

        Retorna a lista de todos os funcionários cadastrados na plataforma.
        É possível realizar filtros na hora de realizar a busca. Abaixo estão os filtros válidos:
        * `logic` - Usado para dizer qual tipo de operador lógico utilizar para comparação. Valores válidos: `AND` e `OR`.O valor padrão é `AND`.
        * `operator` - Usado para informar que tipo de comparação deve ser feita. Valores válidos: ,`EQUAL`,`NOT_EQUAL`,`CONTAINS`,`LESS_THAN`,`MORE_THAN`,`LESS_THAN_OR_EQUAL`,`MORE_THAN_OR_EQUAL`O valor padrão é ,`CONTAINS`
        * `name` - Nome do funcionário.
        * `jot_title` - Cargo do funcionário.
        * `email` - Email do funcionário.
    """
    employees = Employees()
    filters = request.args.to_dict()
    
    employees = Employees()
    data = []

    if not filters:
        data = employees.list()
    else:
        data = employees.search(filters)

    return jsonify({
        "success": True,
        "data": data
    }), 200

@employees_bp.route('/<int:employee_id>', methods=['GET'])
@employees_bp.response(200, GetEmployeesByIDResponseSchema, description="Funcionário encontrado")
@employees_bp.response(404, GetEmployeesByIDResponseNoutFoundSchema, description="Funcionário não encontrado")
@employees_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_employee_by_id(employee_id):
    """Buscar funcionário pelo ID

        Faz a busca de um funcionário pelo ID e retorna erro se não encontrar.
    """
    employees = Employees()
    employee = employees.get_by_id(employee_id)
    if employee: 
        return jsonify({
            "success": True,
            "data": employee
        }), 200
    
    return jsonify({
        "success": False,
        "point": "get_employee_by_id",
        "message": "Funcionário não encontrado"
    }), 404


@employees_bp.route('/', methods=['POST'])
@jwt_required()
def create_employee():
    data = request.json

    validation_error = schemaValidate(["name", "job_title", "email", "password"], data)

    if validation_error:
        return validation_error
    
    employees = Employees()
    employees.create(data)

    return jsonify({ "success": True }), 201

@employees_bp.route('/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    employees = Employees()
    try:
        employees.delete(employee_id)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "delete_employee",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

@employees_bp.route('/<int:employee_id>', methods=['PATCH'])
@jwt_required()
def update_employee(employee_id):
    data = request.json
    validation_error = schemaValidate(["id", "created_at"], data, False)

    if validation_error:
        return validation_error
    
    employees = Employees()
    try:
        employees.update(employee_id, data)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "update_employee",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

        