from flask import Flask
from flask_migrate import Migrate
from app.config import load_configurations, configure_logging
from app.databases.db_init import init_db, db
from app.whatsapp_webhook import webhook_blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, origins="http://localhost:5173")

    # Database configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'  # Modify for your production DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Flask extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Load configurations and logging settings
    load_configurations(app)
    configure_logging()
    
    init_db(app)


    # Register blueprints
    app.register_blueprint(webhook_blueprint)

    return app
