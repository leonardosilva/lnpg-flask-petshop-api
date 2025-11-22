from flask import jsonify, request
from flask_smorest import Blueprint
from ..services.auth import Auth
from ..utils.validate import schemaValidate, ValidationFailedSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from ..schemas.auth import LoginSchema, LoginResponseSchema, LoginResponseFailedSchema, RefreshSchema, RefreshResponseFailedSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@auth_bp.doc(
    requestBody={
        "content": {
            "application/json": {
                "schema": LoginSchema 
            }
        },
        "required": True 
    }
)
@auth_bp.response(422, ValidationFailedSchema, description="Falha na validação dos campos")
@auth_bp.response(400, LoginResponseFailedSchema, description="Falha na autenticação ou erro de validação.")
@auth_bp.response(200, LoginResponseSchema, description="Login bem-sucedido.")
def login():
    """Realizar o login do usuário

    Recebe email e senha para autenticação.
    Se as credenciais estiverem corretas, retorna:
    * **access_token**: Para acessar rotas privadas.
    * **refresh_token**: Para renovar o acesso.
    """
    data = request.json

    validation_error = schemaValidate(["email", "password"], data)

    if validation_error:
        return validation_error
    
    auth = Auth()
    try:
        response = auth.login(data)
        return response, 200
    except Exception as err:
        error_body = {
            "success": False,
            "point": "login",
            "message": str(err)
        }
        return jsonify(error_body), 400

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@auth_bp.doc(security=[{"bearerAuth": []}])
@auth_bp.response(200, RefreshSchema, description="Sucesso ao gerar novo token de acesso.")
@auth_bp.response(401, RefreshResponseFailedSchema, description="Falha ao gerar novo token de acesso.")
def refresh():
    """Gerar um novo token de acesso

    Envie no header Authorization o refresh token retornado no login.

    `Authorization: Bearer <refresh_token>`

    será retornado um novo `access_token` caso o `refresh_token` seja válido.
    """
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    
    return jsonify({"access_token": new_access_token}), 200