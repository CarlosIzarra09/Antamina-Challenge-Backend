from src.database.extensions import db, ma
from datetime import datetime

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.JSON)

    def __init__(self, data) -> None:
        self.data = data

class SummarySchema(ma.Schema):
    class Meta:
        fields = ("id", "data")

summary_schema = SummarySchema()
summaries_schema = SummarySchema(many=True)


class SummaryData:
    name_sensor: str
    average_value: float
    unit: str
    timestamp: datetime

    def __init__(self, name_sensor, average_value, unit, timestamp) -> None:
        self.name_sensor = name_sensor
        self.average_value = average_value
        self.unit = unit
        self.timestamp = timestamp
    
    def to_dict(self):
        return {
            'name_sensor': self.name_sensor,
            'average_value': self.average_value,
            'unit': self.unit,
            'timestamp': self.timestamp
        }