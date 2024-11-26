import json
import csv
import pandas as pd
import os

json_data1 = {
    "_id": "507f1f77bcfrtrd799439011",
    "Weight": 64,
    "BMI": 22.28,
    "Water %": 44.75,
    "Bone Mass": 8,
    "Muscle Mass": 44.4,
    "Fat %": 18.64,
    "Visceral Fat": 15,
    "Metabolic Age": 28,
    "BMR": 1602
}

json_data2 = {
    "_id": "507f1f77bcf86cd799439011",
    "Weight": 65,
    "BMI": 22.28,
    "Water %": 44.75,
    "Bone Mass": 10,
    "Muscle Mass": 44.4,
    "Fat %": 20,
    "Visceral Fat": 7.93,
    "Metabolic Age": 28,
    "BMR": 1602
}

json_data3 = {
    "_id": "507f1f77bcf86cd734539011",
    "Weight": 70,
    "BMI": 22.28,
    "Water %": 44.75,
    "Bone Mass": 8,
    "Muscle Mass": 44.4,
    "Fat %": 18.64,
    "Visceral Fat": 7.93,
    "Metabolic Age": 28,
    "BMR": 1602
}


_id = "507f1f77bcf86cd799439011"

class LocalDataManagement():
    fieldnames = ["_id", "Weight", "BMI", "Water %", "Bone Mass", "Muscle Mass", "Fat %", "Visceral Fat", "Metabolic Age", "BMR"]
    file_path = "user_data.csv"
    
    def __init__(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
        
        
    def is_user_exist(self, user_id):
        if os.path.exists(self.file_path):
            with open(self.file_path) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['_id'] == user_id :
                        return True
                return False
            
    def append_user_data(self, data):
        temp_list = []
        temp_list.append(data)
        
        if os.path.exists(self.file_path):
            with open(self.file_path, "a", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writerows(temp_list)            
                print(f"Row with id {data['_id']} appended successfully.")

    def get_user_data(self, user_id):
        if os.path.exists(self.file_path):
            with open(self.file_path) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['_id'] == user_id :
                        return row
                print(f"Row with id {user_id} not found.")
                return {}
            
    def update_user_data(self, data):
        df = pd.read_csv(self.file_path)
        
        row_index = df[df['_id'] == data['_id']].index
        
        if not row_index.empty:
            df.loc[row_index, data.keys()] = list(data.values())
            
            df.to_csv(self.file_path, index=False)
            print(f"Row with id {data['_id']} updated successfully.")
        else:
            print(f"Row with id {data['_id']} not found.")
            
    def delete_user_data(self, user_id):
        df = pd.read_csv(self.file_path)
        
        df = df[df['_id'] != user_id]
        
        df.to_csv(self.file_path, index=False)
        print(f"Row with id {user_id} deleted successfully.")
    
my_data = LocalDataManagement()
print(my_data.delete_user_data("507f1f77bcf86cd734539011"))
