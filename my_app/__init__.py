import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
from flask_smorest import Api
import textwrap

def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True) 
    
    app.config["API_TITLE"] = "Petshop FLASK API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
    app.config["API_SPEC_OPTIONS"] = {
        "info": {
            "description": textwrap.dedent("""
            API voltada para o desenvolvimento de um sistema de Petshop.

            ### Como Autenticar
            Você precisa obter um token JWT na rota `/auth/login` e enviá-lo no header:
            `Authorization: Bearer <seu_token>`

            ### Funcionalidades
            * Gerenciamento de Clientes
            * Agendamentos
            * Controle de Pets
            * Gerenciamentos de funcionários
            * Gerenciamento de serviços

            ### Desenvolvedores
            * [Marcos Vinicius](https://github.com/mvinib)
            * [Abel Lucas](https://github.com/abellucas-dev)
            * [David Emiliano](https://github.com/davidemiliano666)
            * [Leonardo Silva](https://github.com/leonardosilva)
                                           
            """)
        },
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    }

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    api = Api(app)

    from .api.clients import clients_bp
    from .api.appointments import appointments_bp
    from .api.pets import pets_bp
    from .api.employees import employees_bp
    from .api.auth import auth_bp

    api.register_blueprint(auth_bp, url_prefix='/auth')
    api.register_blueprint(clients_bp, url_prefix='/clients')
    api.register_blueprint(appointments_bp, url_prefix='/appointments')
    api.register_blueprint(pets_bp, url_prefix='/pets')
    api.register_blueprint(employees_bp, url_prefix='/employees')

    jwt = JWTManager(app)
    
    @jwt.unauthorized_loader
    def custom_unauthorized_response(err):
        return jsonify({
            "success": False,
            "point": "authentication",
            "message": "Envie um header Authorization"
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload): 
        token_type = jwt_payload.get('type', 'access')
        
        if token_type == 'refresh':
            return jsonify({
                "success": False,
                "point": "renew_token",
                "message": "Sessão expirada. Faça login novamente."
            }), 401
        
        return jsonify({
            "success": False,
            "message": "Token de acesso expirado. Use o refresh token para obter um novo.",
            "point": "access_token_expired"
        }), 401
    
    @app.route('/health')
    def health_check():
        return "OK", 200
    

    return app