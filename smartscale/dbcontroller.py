from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import sys
sys.path.append('../')  
from calc_metrics import *

# URI kết nối MongoDB Atlas
URI = "mongodb+srv://admin:admin123@cluster0.h40dz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(URI)
db = client['health_app']
collection = db['users']



class dbcontroller:
    body_metrics = {}
    # def __init__(self):
        
        
    @classmethod
    def get_body_metrics(cls):
        return cls.body_metrics
        
    @classmethod
    def clear_body_metrics(cls):
        cls.body_metrics.clear()
    
    @staticmethod
    def push_data_to_db(cls, user_id, height, age):   
        new_record = {
            "date": datetime.now(),
            "age": age,
            "height": height,
        }

        new_record.update(cls.body_metrics)
        current_data = collection.find_one({"id": user_id})
        if current_data:
            records = current_data.get("records", [])
            records.append(new_record)
            records = sorted(records, key=lambda x: x["date"], reverse=True)
            collection.update_one(
                {"id": user_id},
                {"$set": {"records": records}}
            )
            print(f"Đã thêm thông tin mới vào records cho user với ID {user_id}.")
            return True
    
    @classmethod
    def process_data(cls, user_id, weight):
        result = collection.find_one(
            {"id": user_id},
            {"_id": 0, "dateOfBirth": 1, "gender": 1,"activityFactor": 1, "records.height": 1}
        )

        if result:
            gender = result.get("gender")
            date_of_birth = result.get("dateOfBirth")
            activity_factor = float(result.get("activityFactor"))
            records = result.get("records", [])
            height = int(records[0].get("height", None) if records else None)
            if date_of_birth:
                current_date = datetime.now()
                age = int(current_date.year - date_of_birth.year - ((current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day)))
            else:
                age = "Không rõ"
            
        if height and weight and age and gender and activity_factor:
            cls.body_metrics = get_body_metrics(height, weight, age, gender, activity_factor) 
            cls.push_data_to_db(cls, user_id, height, age)
        else:
            print(f"Không tìm thấy user với ID {user_id}.")
            return False
        
    
    

