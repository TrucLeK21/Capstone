import express from "express";
import User from "../models/user.js";
import protect from "../middleware/middleware.js";
import { Schema } from "mongoose";

const router = express.Router();

const nameMap = {
  height: "Chiều cao",
  weight: "Cân nặng",
  date: "Ngày đo",
  age: "Tuổi",
  bmi: "BMI",
  bmr: "BMR",
  tdee: "TDEE",
  lbm: "Khối lượng không mỡ",
  fatPercentage: "Phần trăm mỡ",
  waterPercentage: "Phần trăm nước",
  boneMass: "Khối lượng xương",
  muscleMass: "Khối lượng cơ",
  proteinPercentage: "Phần trăm protein",
  visceralFat: "Mỡ nội tạng",
  idealWeight: "Cân nặng lý tưởng",
};

const unitMap = {
  height: "cm",
  weight: "kg",
  age: null,
  bmi: null,
  bmr: "kcal",
  tdee: "kcal",
  lbm: "kg",
  fatPercentage: "%",
  waterPercentage: "%",
  boneMass: "kg",
  muscleMass: "kg",
  proteinPercentage: "%",
  visceralFat: null,
  idealWeight: "kg",
  date: null,
};
//put api

router.put(`/update`, protect, async (req, res) => {
  const { fullName, dateOfBirth, gender, height, weight, activityFactor } = req.body;

  try {
    const user = await User.findOne({ id: req.user.id });
    if (!user) {
      return res.status(404).json({ message: "user not found" });
    }

    if (fullName) user.fullName = fullName;
    
    const updatedUser = await user.addRecord({ weight, height, dateOfBirth, gender, activityFactor });
    
    console.log("update user:");
    console.log(user);

    res.status(200).json({
      message: 'Cập nhật user thành công',
      user: updatedUser,
    });

  } catch (e) {
    res.status(500).json(e.message);
  }
});

// get api
router.get(`/profile`, protect, async (req, res) => {
  try {
    let user = await User.findOne({ id: req.user.id });


    if (!user) {
      return res.status(404).json({ message: "user not found" });
    }
    console.log(user);
    res.status(200).json(user);
  } catch (e) {
    res.status(500).json(e.message);
  }
});

//get lastest record 
router.get(`/lastestRecord`, protect, async (req, res) => {
  try {
    let user = await User.findOne({ id: req.user.id });
    if (!user) {
      return res.status(404).json({ message: "user not found" });
    }

    const latestRecord = user.records.sort((a, b) => new Date(b.date) - new Date(a.date))[0].toObject();
    console.log(latestRecord);
    const result = Object.keys(latestRecord).map((key) => ({
      key: key,
      name: nameMap[key] || key,
      value: latestRecord[key] || null,
      unit: unitMap[key] ||null
    }));
    
    return res.status(200).json(result);
  }
 catch(e) {
  res.status(500).json(e.message);
}});

export default router;