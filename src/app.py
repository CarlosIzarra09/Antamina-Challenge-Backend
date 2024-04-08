from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

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

class MeasurementDetailSchema(ma.Schema):
    class Meta:
        fields = ("id", "name_sensor", "value", "unit", "timestamp", "summary_id")


class SummarySchema(ma.Schema):
    class Meta:
        fields = ("id", "data")


measurement_detail_schema = MeasurementDetailSchema()
measurements_detail_schema = MeasurementDetailSchema(many=True)

summary_schema = SummarySchema()
summaries_schema = SummarySchema(many=True)

@app.route("/api/v1/list", methods=["GET"])
def get_summaries():
    all_summaries = Summary.query.all()
    result = summaries_schema.dump(all_summaries)
    return summaries_schema.jsonify(result)

@app.route("/api/v1/load", methods=["POST"])
def load_data():
    if not request.json or "data" not in request.json:
        return jsonify({"error": "Missing data field in JSON"}), 400

    data = request.json['data']
    
    if not isinstance(data, list):
        return jsonify({"error": "data must be a list"}), 400

    # Realizamos el calculo
    sum_values = {}
    count_value = {}
    unit_values = {}
    timestamp_values = {}
    
    # arreglo para json summary
    summary_array = []
    measurement_array = []

    for item in data:
        nameSensor = item["name"]
        value = item["value"]
        unit = item["unit"]
        time = item["timestamp"]
        
        measurement_array.append(MeasurementDetail(name_sensor=nameSensor,unit=unit,timestamp=time,value=value,summary_id=0))
        
        if nameSensor not in sum_values:
            sum_values[nameSensor] = value
            count_value[nameSensor] = 1

            unit_values[nameSensor] = unit
            timestamp_values[nameSensor] = time
        else:
            sum_values[nameSensor] += value
            count_value[nameSensor] += 1


    for nameSensor in sum_values:
        avg = round(sum_values[nameSensor] / count_value[nameSensor],5)
        summary_data = SummaryData(
            nameSensor, avg, unit_values[nameSensor], timestamp_values[nameSensor]
        )
        summary_array.append(summary_data.to_dict())
    
    ##Insercion en Db
    new_summary = Summary(summary_array)
    db.session.add(new_summary)
    db.session.commit()
    
    #Insercion de los measurument_detail
    for item in measurement_array:
        item.summary_id = new_summary.id
        db.session.add(item)
        db.session.commit()
        
    return summary_schema.jsonify(new_summary)



if __name__ == "__main__":
    app.run(debug=True)
