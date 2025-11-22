from flask import  jsonify, request
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from ..services.appointments import Appointments
from ..utils.validate import schemaValidate, ValidationFailedSchema
from ..schemas.appointments import GetAppointmentResponseSchema, GetAppointmentsByIDResponseNoutFoundSchema, GetAppointmentsByIDResponseSchema, CreateAppointmentResponseFailedSchema, CreateAppointmentSchema, DeleteAppointmentResponseFailedSchema, UpdateAppointmentSchema, UpdateAppointmentResponseFailedSchema
from ..schemas.generic import GenericSuccessSchema

appointments_bp = Blueprint('appointments', __name__, description="Gestão de Agendamentos")

@appointments_bp.route('/', methods=['GET'])
@appointments_bp.response(200, GetAppointmentResponseSchema, description="Lista de agendamentos")
@appointments_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_Appointments():
    """Buscar lista de agendamentos

        Retorna a lista de todos os agendamentos cadastrados na plataforma.
        É possível realizar filtros na hora de realizar a busca. Abaixo estão os filtros válidos:
        * `logic` - Usado para dizer qual tipo de operador lógico utilizar para comparação. Valores válidos: `AND` e `OR`.O valor padrão é `AND`.
        * `operator` - Usado para informar que tipo de comparação deve ser feita. Valores válidos: ,`EQUAL`,`NOT_EQUAL`,`CONTAINS`,`LESS_THAN`,`MORE_THAN`,`LESS_THAN_OR_EQUAL`,`MORE_THAN_OR_EQUAL`O valor padrão é ,`CONTAINS`
        * `pet_id` - ID do pet.
        * `service_id` - ID do serviço.
        * `employee_id` - ID do funcionário.
        * `pet` - Nome do pet.
        * `service` - Nome do serviço.
        * `employee` - Nome do funcionário.
        * `status` - Status do agendamento. Valores válidos: `scheduled`, `finished` e `canceled`.
    """
        
    appointments = Appointments()
    filters = request.args.to_dict()
    
    appointments = Appointments()
    data = []

    if not filters:
        data = appointments.list()
    else:
        data = appointments.search(filters)

    return jsonify({
        "success": True,
        "data": data
    }), 200

@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
@appointments_bp.response(200, GetAppointmentsByIDResponseSchema, description="Agendamento encontrado")
@appointments_bp.response(404, GetAppointmentsByIDResponseNoutFoundSchema, description="Agendamento não encontrado")
@appointments_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_appointment_by_id(appointment_id):
    """Buscar agendamento pelo ID

        Faz a busca de um agendamento pelo ID e retorna erro se não encontrar.
    """
    appointments = Appointments()
    appointment = appointments.get_by_id(appointment_id)
    if appointment: 
        return jsonify({
            "success": True,
            "data": appointment
        }), 200
    
    return jsonify({
        "success": False,
        "point": "get_appointment_by_id",
        "message": "Agendamento não encontrado"
    }), 404


@appointments_bp.route('/', methods=['POST'])
@appointments_bp.doc(security=[{"bearerAuth": []}])
@appointments_bp.doc(
    requestBody={
        "content": {
            "application/json": {
                "schema": CreateAppointmentSchema 
            }
        },
        "required": True 
    }
)
@appointments_bp.response(422, ValidationFailedSchema, description="Falha na validação dos campos")
@appointments_bp.response(400, CreateAppointmentResponseFailedSchema, description="Falha ao criar o agendamento")
@appointments_bp.response(201, GenericSuccessSchema, description="Agendamento criado com sucesso")
@jwt_required()
def create_appointment():
    """Criar novo agendamento
    """
    data = request.json

    validation_error = schemaValidate(["pet_id", "service_id", "employee_id", "scheduled_at"], data)

    if validation_error:
        return validation_error
    
    appointments = Appointments()
    try:
        appointments.create(data)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "create_appointment",
            "message": str(err)
        }), 400

    return jsonify({ "success": True }), 201

@appointments_bp.route('/<int:appointment_id>', methods=['DELETE'])
@appointments_bp.doc(security=[{"bearerAuth": []}])
@appointments_bp.response(200, GenericSuccessSchema, description="Agendamento deletado com sucesso")
@appointments_bp.response(400, DeleteAppointmentResponseFailedSchema, description="Agendamento não encontrado")
@jwt_required()
def delete_appointment(appointment_id):
    """Deletar agendamento
    """
    appointments = Appointments()
    try:
        appointments.delete(appointment_id)
    except Exception as err:
        return jsonify({
            "success": False,
            "point": "delete_appointment",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

@appointments_bp.route('/<int:appointment_id>', methods=['PATCH'])
@appointments_bp.doc(security=[{"bearerAuth": []}])
@appointments_bp.doc(
    requestBody={
        "content": {
            "application/json": {
                "schema": UpdateAppointmentSchema 
            }
        },
        "required": False 
    }
)
@appointments_bp.response(422, ValidationFailedSchema, description="Falha na validação dos campos")
@appointments_bp.response(400, UpdateAppointmentResponseFailedSchema, description="Agendamento não encontrado")
@appointments_bp.response(200, GenericSuccessSchema, description="Agendamento editado com sucesso")
@jwt_required()
def update_appointment(appointment_id):
    """Editar agendamento

    Todos os campos do agendamento podem ser editados. Exceto: 
    * id
    * pet_id

    O campo `status` só aceita os valores: `scheduled`, `finished`, `canceled`
    """
    data = request.json
    validation_error = schemaValidate(["id", "pet_id"], data, False)

    if validation_error:
        return validation_error
    
    status = data.get("status", None)
    if status:
        status_allowed = ["scheduled", "finished", "canceled"]
        if status not in status_allowed:
            return jsonify({
                "success": False,
                "point": "update_appointment",
                "message": f"O status informado é inválido. Valores válidos: {", ".join(status_allowed)}"
        }), 422
    
    appointments = Appointments()
    try:
        appointments.update(appointment_id, data)
    except Exception as err:

        return jsonify({
            "success": False,
            "point": "update_appointment",
            "message": str(err)
        }), 400
    
    return jsonify({ "success": True }), 200

        