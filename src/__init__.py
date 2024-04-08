from flask import Flask
from src.routes import IndexRoutes



def init_app(config):
    
    app = Flask(__name__)
    # Configuration
    app.config.from_object(config)
    
    # Blueprints
    app.register_blueprint(IndexRoutes.main, url_prefix='/api/v1')
    
    return app