from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from Code.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('Code.config.Config')
    db.init_app(app)
    migrate = Migrate(app, db)

    from Code.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from Code.admin.routes import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from Code.service_management.routes import service_management as service_management_blueprint
    app.register_blueprint(service_management_blueprint, url_prefix='/service_management')

    from Code.service_requests.routes import service_requests as service_requests_blueprint
    app.register_blueprint(service_requests_blueprint, url_prefix='/service_requests')

    from Code.professional_actions.routes import professional_actions as professional_actions_blueprint
    app.register_blueprint(professional_actions_blueprint, url_prefix='/professional_actions')

    
    @app.route('/')
    def home():
        return render_template('home.html')
    
    return app