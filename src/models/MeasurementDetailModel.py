from src.database.extensions import db, ma
from datetime import datetime


class MeasurementDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_sensor = db.Column(db.String(20))
    value = db.Column(db.Float)
    unit = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    summary_id = db.Column(db.Integer, db.ForeignKey("summary.id"))
    summary = db.relationship("Summary")

    def __init__(self, name_sensor, value, unit, timestamp, summary_id) -> None:
        self.name_sensor = name_sensor
        self.value = value
        self.unit = unit
        self.timestamp = timestamp
        self.summary_id = summary_id

class MeasurementDetailSchema(ma.Schema):
    class Meta:
        fields = ("id", "name_sensor", "value", "unit", "timestamp", "summary_id")
        
measurement_detail_schema = MeasurementDetailSchema()
measurements_detail_schema = MeasurementDetailSchema(many=True)