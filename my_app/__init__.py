import os
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True) 

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .api.clients import clients_bp
    from .api.appointments import appointments_bp

    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')

    @app.route('/health')
    def health_check():
        return "OK", 200
    
    return app