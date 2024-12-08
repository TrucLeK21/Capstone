import express from "express";
import User from "../models/user.js";
import jwt from "jsonwebtoken";

const router = express.Router();

const generateToken = (userId) => {
    return jwt.sign({ id: userId }, process.env.JWT_SECRET, {
        expiresIn: process.env.JWT_EXPIRES_IN, // Thời hạn của token
    });
};


router.post(`/register`, async (req, res) => {
    console.log("Result", req.body);
    const {username, password} = req.body;
  
    try {
        let user = await User.findOne({username});
        if(user)
        {
            return res.status(400).json({ message: 'user already exists' });
        }
        user = new User({username, password});
        await user.save();

        res.status(200).json({ message: 'success'});
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
  });

  router.post('/login', async (req, res) => {
    const {username, password} = req.body;

    try {
        let user = await User.findOne({username});

        if(!user)
        {
            return res.status(400).json({ message: 'Incorrect username or password' });
        }
        
        const isMatch = await user.matchPassword(password);
        if(!isMatch){
            return res.status(400).json({ message: 'Incorrect username or password' });
        }
        const token = generateToken(user.id);
        console.log(token);

        if(user.fullName != null && user.dateOfBirth != null && user.gender != null && user.activityFactor != null && user.records.length > 0)
        {
            res.status(200).json({ message: 'success', token: token});
        }
        else 
        {
            res.status(202).json({ message: 'success but missing metrics', token: token});
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }

  });
  
  router.post('/logout', async (req, res) => {
    res.status(200).json({message: 'logout successfully'});
  })

  export default router;