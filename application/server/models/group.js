
import mongoose from "mongoose";


const groupSchema = new mongoose.Schema({
    id: {
        type: Number,
        unique: true
    },
    name: {
        type: String,
        required: true,
        trim: true,
        minlength: 5
    },
    createdDate: {
        type: Date,
        default: Date.now,
    },
    members: {
        type: [Number], // Mảng các ID (kiểu Number)
        default: function () {
            return [this.owner]; // Mặc định chứa ID của `owner`
        }
    },
    owner: {
        type: Number,
        required: true,
    }
});

export default mongoose.model('Group', groupSchema, 'group');