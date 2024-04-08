
from src.models.MeasurementDetailModel import MeasurementDetail
from src.models.SummaryModel import Summary, SummaryData
from src.database.extensions import db

# Services
from src.services.SummaryService import SummaryService

class MeasurementDetailService:
    
    @classmethod
    def add_measure_data(cls,data):
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
        new_summary = SummaryService.add_summary(summary_array)
        
        #Insercion de los measurument_detail
        for item in measurement_array:
            item.summary_id = new_summary.id
            db.session.add(item)
            db.session.commit()
            
        return new_summary