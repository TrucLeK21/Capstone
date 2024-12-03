from pymongo import MongoClient
import json
from bson.objectid import ObjectId
from datetime import datetime
import sys
sys.path.append('../')  
from calc_metrics import *

# URI kết nối MongoDB Atlas
uri = "mongodb+srv://admin:admin123@cluster0.h40dz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
db = client['health_app']
collection = db['users']

# Thêm dữ liệu mẫu vào MongoDB (tùy chọn)
json_data_list = [
    {
        "id": 100,
        "username": "john_doe",
        "password": "password123",
        "fullName": "John Doe",
        "dateOfBirth": "1990-05-15",
        "gender": "male",
        "activity_factor": "1.375",
        "group": 1,
        "records": [
            {
                "date": "2024-11-25T10:30:00Z",
                "age": 34,
                "height": 180,
                "weight": 75,
                "bmi": 23.15,
                "bmr": 1750,
                "tdee": 2500,
                "lbm": 58.5,
                "fatPercentage": 20.0,
                "waterPercentage": 50.0,
                "boneMass": 7.0,
                "muscleMass": 40.0,
                "proteinPercentage": 18.0,
                "visceralFat": 10.0,
                "idealWeight": 72.0
            }
        ]
    },
    {
        "id": 200,
        "username": "jane_smith",
        "password": "securepass456",
        "fullName": "Jane Smith",
        "dateOfBirth": "1995-09-23",
        "gender": "female",
        "activity_factor": "1.2",
        "group": 2,
        "records": []
    }
]

# Thêm dữ liệu mẫu nếu cần
try:
    result = collection.insert_many(json_data_list)
    print(f"Dữ liệu đã được chèn với các ID: {result.inserted_ids}")
except Exception as e:
    print(f"Lỗi khi chèn dữ liệu (có thể dữ liệu đã tồn tại): {e}")

# Lấy dữ liệu dựa vào id và weight
user_id = 100
weight = 60

result = collection.find_one(
    {"id": user_id},
    {"_id": 0, "dateOfBirth": 1, "gender": 1,"activity_factor": 1, "records.height": 1}
)

if result:
    gender = result.get("gender")
    date_of_birth = result.get("dateOfBirth")
    activity_factor = float(result.get("activity_factor"))
    records = result.get("records", [])
    height = int(records[0].get("height", None) if records else None)
    if date_of_birth:
        current_date = datetime.now()
        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
        age = int(current_date.year - date_of_birth.year - ((current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day)))
    else:
        age = "Không rõ"
    
if height and weight and age and gender and activity_factor:
    body_metrics = get_body_metrics(height, weight, age, gender, activity_factor)
        
    print(f"{'Chỉ số':<15}{'Giá trị':<10}{'Đơn vị':<10}")
    print("=" * 35)
    for metric in body_metrics:
        print(f"{metric['name']:<15}{metric['value']:<10}{metric['unit']:<10}")

    new_record = {
        "date": datetime.now().isoformat(),
        "age": age,
        "height": height,
    }

    for metric in body_metrics:
        name = metric["name"]
        value = metric["value"]
        new_record[name.replace(" ", "").lower()] = value

    print(new_record)

# current_data = collection.find_one({"id": user_id})
# if current_data:
#     records = current_data.get("records", [])
#     records.append(new_record)
#     records = sorted(records, key=lambda x: x["date"], reverse=True)
#     collection.update_one(
#         {"id": user_id},
#         {"$set": {"records": records}}
#     )
#     print(f"Đã thêm thông tin mới vào records cho user với ID {user_id}.")
# else:
#     print(f"Không tìm thấy user với ID {user_id}.")
