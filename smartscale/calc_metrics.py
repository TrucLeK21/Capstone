from math import floor
from datetime import datetime


# Calculate age based on date of birth string (dob_str) in format "dd/mm/yyyy"
def calculate_age(dob_str):
    dob = datetime.strptime(dob_str, "%d/%m/%Y")
    today = datetime.today()
    # Calculate age based on the difference between current year and birth year
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

# Check if the value exceeds the allowed limit, if so adjust to the limit
def check_val_overflow(value, minimum, maximum):
    return max(min(value, maximum), minimum)

# Calculate BMI based on height (cm) and weight (kg)
def get_bmi(height, weight):
    height_in_meters = height / 100  
    bmi = weight / (height_in_meters ** 2)  
    return round(bmi, 2)

# Calculate basal metabolic rate (BMR) and total daily energy expenditure (TDEE)
def get_bmr_tdee(weight, height, age, gender, activity_factor):
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    tdee = bmr * activity_factor
    return int(bmr), round(tdee, 2)

# Assess BMI and provide ideal weight suggestions if needed
def evaluate_bmi(bmi, height, weight):
    if bmi < 18.5:
        status = "Thiếu cân"
        ideal_weight = 18.5 * (height / 100) ** 2  
        weight_diff = ideal_weight - weight
    elif bmi < 24.9:
        status = "Bình thường"
        weight_diff = 0  
    elif bmi < 29.9:
        status = "Thừa cân"
        ideal_weight = 24.9 * (height / 100) ** 2  
        weight_diff = weight - ideal_weight
    else:
        status = "Béo phì"
        ideal_weight = 24.9 * (height / 100) ** 2
        weight_diff = weight - ideal_weight
    
    return status, round(weight_diff, 2)

# Give feedback on basic daily energy needs
def evaluate_bmr(bmr):
    return f"Cần {bmr} kcal mỗi ngày để duy trì năng lượng cơ bản."

# Give feedback on total daily energy consumptio
def evaluate_tdee(tdee):
    return f"Cần {tdee} kcal mỗi ngày để duy trì cân nặng hiện tại."

# Calculate fat-free body mass (LBM)
def get_lbm(height, weight, gender):
    if gender == 'male':
        # LBM Formula for Men
        lbm = (0.32810 * weight) + (0.33929 * height) - 29.5336
    else:
        # LBM Formula for Women
        lbm = (0.29569 * weight) + (0.41813 * height) - 43.2933
    return round(lbm, 2)

# Calculate body fat percentage
def get_fat_percentage(gender, age, weight, height):
    lbm = get_lbm(height, weight, gender)  
    # Calculate body fat percentage based on gender-specific formulas
    fat_percentage = (1.20 * (weight - lbm) / weight * 100) + (0.23 * age) - (10.8 if gender == 'male' else 0) - 5.4
    return round(check_val_overflow(fat_percentage, 5, 75), 2) 

# Calculate the percentage of water in the body
def get_water_percentage(gender, age, weight, height):
    fat_percentage = get_fat_percentage(gender, age, weight, height)
    # Formula for calculating water percentage based on body fat percentage
    water_percentage = (100 - fat_percentage) * (0.55 if gender == 'male' else 0.49)
    return round(check_val_overflow(water_percentage, 35, 75), 2)  

# Calculate bone mass in the body
def get_bone_mass(height, weight, gender):
    lbm = get_lbm(height, weight, gender)  
    # Formula for calculating bone mass based on LBM
    bone_mass = lbm * (0.175 if gender == 'male' else 0.15)
    return round(check_val_overflow(bone_mass, 0.5, 8), 2)  

# Calculate muscle mass in the body
def get_muscle_mass(gender, age, weight, height):
    fat_mass = weight * (get_fat_percentage(gender, age, weight, height) / 100)  
    bone_mass = get_bone_mass(height, weight, gender)  
    # Calculate muscle mass by subtracting fat and bone mass from weight
    muscle_mass = weight - fat_mass - bone_mass
    return round(check_val_overflow(muscle_mass, 10, 120), 2)  

# Calculate the percentage of protein in the body
def get_protein_percentage(gender, age, weight, height, orig=True):
    muscle_mass = get_muscle_mass(gender, age, weight, height)  
    water_mass = weight * (get_water_percentage(gender, age, weight, height) / 100)  
    # Formula for calculating protein percentage in the body based on muscle and water content
    protein_percentage = (muscle_mass * 0.19 + water_mass * 0.16) / weight * 100
    return round(check_val_overflow(protein_percentage, 5, 32), 2)  

# Calculate visceral fat
def get_visceral_fat(gender, height, weight, age):
    # Formula for calculating visceral fat based on gender, height and weight
    visceral_fat = weight * 0.1 + age * 0.05 + (0.1 * (weight / height)) if gender == 'male' else weight * 0.08 + age * 0.06 + (0.08 * (weight / height))
    return round(check_val_overflow(visceral_fat, 1, 50), 2) 

# Calculate ideal weight based on gender and height
def get_ideal_weight(gender, height, orig=True):
    # Formula for calculating ideal weight
    ideal_weight = (height - 100 + (height / 100)) if gender == 'male' else (height - 100 + ((height / 100) * 0.9))
    return round(check_val_overflow(ideal_weight, 5.5, 198), 2)  

def get_body_metrics(height, weight, age, gender, activity_factor):

    bmi = get_bmi(height, weight)
    bmr, tdee = get_bmr_tdee(weight, height, age, gender, activity_factor)
    lbm = get_lbm(height, weight, gender)
    fat_percentage = get_fat_percentage(gender, age, weight, height)
    water_percentage = get_water_percentage(gender, age, weight, height)
    bone_mass = get_bone_mass(height, weight, gender)
    muscle_mass = get_muscle_mass(gender, age, weight, height)
    protein_percentage = get_protein_percentage(gender, age, weight, height, orig=True)
    visceral_fat = get_visceral_fat(gender, height, weight, age)
    idealWeight = get_ideal_weight(gender, height, orig=True)
   
    body_metrics = {
    "weight": weight,
    "bmi": bmi,
    "bmr": bmr,
    "tdee": tdee,
    "lbm": lbm,
    "fat_percentage": fat_percentage,
    "water_percentage": water_percentage,
    "bone_mass": bone_mass,
    "muscle_mass": muscle_mass,
    "protein_percentage": protein_percentage,
    "visceral_fat": visceral_fat,
    "ideal_weight": idealWeight
    }
    
    return body_metrics
