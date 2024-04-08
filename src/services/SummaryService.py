from src.models.SummaryModel import Summary, summaries_schema
from src.database.extensions import db

class SummaryService:

    @classmethod
    def get_summaries(cls):
        all_summaries = Summary.query.all()
        result = summaries_schema.dump(all_summaries)
        return result

    @classmethod
    def add_summary(cls,data):
        new_summary = Summary(data)
        db.session.add(new_summary)
        db.session.commit()
        return new_summary