from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:password@127.0.0.1/sensors_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class MeasurementDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_sensor = db.Column(db.String(20))
    value = db.Column(db.Float)
    unit = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    summary_id = db.Column(db.Integer, db.ForeignKey("summary.id"))
    summary = db.relationship("Summary")

    def __init__(self, name_sensor, value, unit, timestamp, summary_id):
        self.name_sensor = name_sensor
        self.value = value
        self.unit = unit
        self.timestamp = timestamp
        self.summary_id = summary_id


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.JSON)

    def __init__(self, data):
        self.data = data


with app.app_context():
    db.create_all()
    
    
if __name__ == "__main__":
    app.run(debug=True)
