from flask import Blueprint, jsonify, request
from src.models.MeasurementDetailModel import MeasurementDetail
from src.models.SummaryModel import Summary, SummaryData, summaries_schema, summary_schema

# Services
from src.services.SummaryService import SummaryService
from src.services.MeasurementDetailService import MeasurementDetailService


main = Blueprint('index_blueprint', __name__)

@main.route("/list", methods=["GET"])
def get_summaries():
   summaries = SummaryService.get_summaries()
   return summaries_schema.jsonify(summaries)

@main.route("/load", methods=["POST"])
def load_data():
    if not request.json or "data" not in request.json:
        return jsonify({"error": "Missing data field in JSON"}), 400

    data = request.json['data']
    
    if not isinstance(data, list):
        return jsonify({"error": "data must be a list"}), 400

    new_summary = MeasurementDetailService.add_measure_data(data)
        
    return summary_schema.jsonify(new_summary)