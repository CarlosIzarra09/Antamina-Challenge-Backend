from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from config import config
from src import init_app
from src.database.extensions import db, ma



configuration = config['development']
app = init_app(configuration)


with app.app_context():
    db.init_app(app)
    ma.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run()