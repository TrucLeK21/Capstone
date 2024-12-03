import express from "express";
import protect from "../middleware/middleware";
import group from "../models/group";

const router = express.Router();


// create route

router.post('/create', protect, async(req, res) => {
    
});