import express from "express";
import User from "../models/user.js";
import protect from "../middleware/middleware.js";

const router = express.Router();


//post api

router.put(`/update`, protect, async (req, res) => {
  const { fullName, dateOfBirth,gender, height, weight } = req.body;
    
  try {
      const user = await User.findOne({id: req.user.id});
      if(!user) {
        return res.status(404).json({message: "user not found"});
      }
      
      if(fullName) user.fullName = fullName;
      if(dateOfBirth) user.dateOfBirth = dateOfBirth;
      if(gender) user.gender = gender;
      const latestRecord = user.records
            ?.sort((a, b) => new Date(b.date) - new Date(a.date))[0] || null;
      if(height || weight){
        const newRecords = {
          height: height ? height: latestRecord.height,
          weight: weight ? weight: latestRecord.weight,
        }
        user.records.push(newRecords);
      }
      console.log("update user:");
      console.log(user);
      const updatedUser = await user.save();
        res.status(200).json({
            message: 'Cập nhật user thành công',
            user: updatedUser,
      });

    } catch(e){
      res.status(500).json(e.message);
    }
  });
  
  // get api
  router.get(`/profile`, protect, async (req, res) => {
    try {
      let user = await User.findOne({id: req.user.id});


      if(!user) {
        return res.status(404).json({message: "user not found"});
      }
      console.log(user);
      res.status(200).json(user);
    } catch (e) {
      res.status(500).json(e.message);
    }
  });

  export default router;