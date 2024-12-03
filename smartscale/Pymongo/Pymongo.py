from pymongo import MongoClient
import json
from bson.objectid import ObjectId
from datetime import datetime


# URI kết nối
uri = "mongodb+srv://quanhoangit482212:482212@scaledb.bsgem.mongodb.net/?retryWrites=true&w=majority&appName=ScaleDB"

client = MongoClient(uri)
db = client['ScaleDB']
collection = db['user']

json_data_list = [
    {
    "id": 1,
    "username": "john_doe",
    "password": "password123",
    "fullName": "John Doe",
    "dateOfBirth": "1990-05-15",
    "gender": "male",
    "group": 1,
    "records": [
        {
            "height": 180,
            "weight": 75,
            "date": "2024-11-25T10:30:00Z",
            "age": 34,
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
}
,
    {
    "id": 2,
    "username": "jane_smith",
    "password": "securepass456",
    "fullName": "Jane Smith",
    "dateOfBirth": "1995-09-23",
    "gender": "female",
    "group": 2,
    "records": [
        {
            "height": 165,
            "weight": 60,
            "date": "2024-11-25T15:45:00Z",
            "age": 29,
            "bmi": 22.04,
            "bmr": 1400,
            "tdee": 2000,
            "lbm": 45.6,
            "fatPercentage": 24.0,
            "waterPercentage": 48.0,
            "boneMass": 6.5,
            "muscleMass": 38.0,
            "proteinPercentage": 16.0,
            "visceralFat": 8.0,
            "idealWeight": 55.0
        },
        {
            "height": 165,
            "weight": 58,
            "date": "2024-11-26T10:00:00Z",
            "age": 29,
            "bmi": 21.3,
            "bmr": 1380,
            "tdee": 1980,
            "lbm": 44.5,
            "fatPercentage": 23.5,
            "waterPercentage": 47.5,
            "boneMass": 6.4,
            "muscleMass": 37.5,
            "proteinPercentage": 15.5,
            "visceralFat": 7.5,
            "idealWeight": 55.0
        }
    ]
}

]

# Thêm nhiều dữ liệu vào MongoDB
# try:
#     result = collection.insert_many(json_data_list)
#     print(f"Dữ liệu đã được chèn với các ID: {result.inserted_ids}")
# except Exception as e:
#     print(f"Lỗi khi chèn dữ liệu: {e}")

#Lấy tất cả dữ liệu với id
user_id = 1
result = collection.find_one(
    {"id": user_id},
    {"_id": 0, "dateOfBirth": 1, "gender": 1, "records.height": 1} 
)

if result:
    gender = result.get("gender", "Không rõ")
    date_of_birth = result.get("dateOfBirth")
    height = result.get("records", [{}])[0].get("height", "Không rõ")

    if date_of_birth:
        current_date = datetime.now()
        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
        age = current_date.year - date_of_birth.year - ((current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day))
    else:
        age = "Không rõ"
    
    # In ra dữ liệu
    print(f"Giới tính: {gender}")
    print(f"Tuổi: {age}")
    print(f"Chiều cao: {height}")
else:
    print(f"Không tìm thấy người dùng với ID: {user_id}")

# # Thông tin mới
new_record = {
    "height": 170,
    "weight": 65,
    "date": datetime.now().isoformat(),  # Thời gian hiện tại
    "age": 34,
    "bmi": 22.5,
    "bmr": 1600,
    "tdee": 2200,
    "lbm": 50.5,
    "fatPercentage": 18.5,
    "waterPercentage": 55,
    "boneMass": 3.5,
    "muscleMass": 45,
    "proteinPercentage": 16,
    "visceralFat": 10,
    "idealWeight": 68
}
#Update lên record
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
else:
    print(f"Không tìm thấy user với ID {user_id}.")