import mongoose, { Schema } from "mongoose";
import bcrypt from "bcrypt";
const SALT_ROUNDS = 10;

// Schema định nghĩa User
const userSchema = new mongoose.Schema({
    id: {
        type: Number,
        unique: true,
    },
    username: {
        type: String,
        required: true,
        unique: true,
        trim: true,
        minlength: 3
    },
    password: {
        type: String,
        required: true,
        minlength: 8
    },
    fullName: {
        type: String,

    },
    dateOfBirth: {
        type: Date, // Ngày sinh
    },
    gender: {
        type: String,
        enum: ["male", "female", "other"],
        default: "other"
    },
    group: {
        type: Number,
        default: null,
    },
    records: [
        {
            height: {
                type: Number,
                min: 50,
                max: 250,
            },
            weight: {
                type: Number,
                min: 50,
                max: 250,
            },
            date: {
                type: Date,
                default: Date.now,
            },
            age: {
                type: Number
            },
            bmi: {
                type: Number
            },
            bmr: {
                type: Number
            },
            tdee: {
                type: Number
            },
            lbm: {
                type: Number
            },
            fatPercentage: {
                type: Number
            },
            waterPercentage: {
                type: Number
            },
            boneMass: {
                type: Number
            },
            muscleMass: {
                type: Number
            },
            proteinPercentage: {
                type: Number
            },
            visceralFat: {
                type: Number
            },
            idealWeight: {
                type: Number
            },
        }
    ],

});

userSchema.pre('save', async function (next) {
    const user = this;
    const today = new Date();

    try {
        // Hash mật khẩu nếu có sự thay đổi
        if (user.isModified('password')) {
            const salt = await bcrypt.genSalt(SALT_ROUNDS);
            user.password = await bcrypt.hash(user.password, salt);
        }

        // Tự động set giá trị id
        if (user.isNew) {
            const count = await mongoose.model('User').countDocuments(); // Đếm số lượng user trong collection
            user.id = count + 1; // Gán id bằng số lượng user hiện tại + 1
        }

        // Lấy bản ghi mới nhất trong records (nếu có)
        let latestRecord = user.records
            ?.sort((a, b) => new Date(b.date) - new Date(a.date))[0] || null;

        // Nếu không có bản ghi nào, khởi tạo bản ghi mới
        if (!latestRecord) {
            user.records = [
                {
                    date: today,
                    height: null,
                    weight: null,
                    age: null,
                    bmi: null,
                    bmr: null,
                    tdee: null,
                    lbm: null,
                    fatPercentage: null,
                    waterPercentage: null,
                    boneMass: null,
                    muscleMass: null,
                    proteinPercentage: null,
                    visceralFat: null,
                    idealWeight: null,
                },
            ];
            latestRecord = user.records[0];
        }

        // Dữ liệu từ latestRecord (cập nhật từ bản ghi mới nhất)
        const weightValue = latestRecord.weight;
        const heightValue = latestRecord.height;
        const groupValue = latestRecord.group;

        // Tính toán các chỉ số từ latestRecord
        const isValidDateOfBirth =
            user.dateOfBirth &&
            !isNaN(new Date(user.dateOfBirth)) &&
            new Date(user.dateOfBirth) <= today;

        const age = isValidDateOfBirth
            ? today.getFullYear() - new Date(user.dateOfBirth).getFullYear() - 
              ((today.getMonth() < new Date(user.dateOfBirth).getMonth() || 
                (today.getMonth() === new Date(user.dateOfBirth).getMonth() && 
                 today.getDate() < new Date(user.dateOfBirth).getDate())) ? 1 : 0)
            : null;

        const heightInMeters = heightValue ? heightValue / 100 : null;

        const bmi = weightValue && heightInMeters
            ? parseFloat((weightValue / (heightInMeters ** 2)).toFixed(2))
            : null;

        let bmr = null;
        if (weightValue && heightValue && age !== null) {
            if (user.gender === 'male') {
                bmr = parseFloat((88.362 + (13.397 * weightValue) + (4.799 * heightValue) - (5.677 * age)).toFixed(2));
            } else if (user.gender === 'female') {
                bmr = parseFloat((447.593 + (9.247 * weightValue) + (3.098 * heightValue) - (4.330 * age)).toFixed(2));
            }
        }

        const tdee = bmr ? parseFloat((bmr * 1.2).toFixed(2)) : null; // Mặc định hoạt động nhẹ (activity factor = 1.2)
        const lbm = weightValue && heightValue
            ? parseFloat(((0.32810 * weightValue) + (0.33929 * heightValue) - 29.5336).toFixed(2))
            : null;

        const fatPercentage = weightValue && lbm
            ? parseFloat((100 - (lbm / weightValue) * 100).toFixed(2))
            : null;

        const waterPercentage = fatPercentage
            ? parseFloat(((100 - fatPercentage) * 0.7).toFixed(2))
            : null;

        const boneMass = lbm
            ? parseFloat(((0.18016894 - (lbm * 0.05158)) * -1).toFixed(2))
            : null;

        const muscleMass = weightValue && fatPercentage && boneMass
            ? parseFloat((weightValue - (fatPercentage * 0.01 * weightValue) - boneMass).toFixed(2))
            : null;

        const proteinPercentage = muscleMass && weightValue && waterPercentage
            ? parseFloat(((muscleMass / weightValue) * 100 - waterPercentage).toFixed(2))
            : null;

        const visceralFat = age !== null
            ? parseFloat((1.0 + (age * 0.07)).toFixed(2))
            : null;

        const idealWeight = heightValue
            ? parseFloat(((heightValue - 80) * 0.7).toFixed(2))
            : null;

        // Thêm bản ghi mới vào records
        latestRecord.date = today;
        latestRecord.height = heightValue;
        latestRecord.weight = weightValue;
        latestRecord.age = age;
        latestRecord.bmi = bmi;
        latestRecord.bmr = bmr;
        latestRecord.tdee = tdee;
        latestRecord.lbm = lbm;
        latestRecord.fatPercentage = fatPercentage;
        latestRecord.waterPercentage = waterPercentage;
        latestRecord.boneMass = boneMass;
        latestRecord.muscleMass = muscleMass;
        latestRecord.proteinPercentage = proteinPercentage;
        latestRecord.visceralFat = visceralFat;
        latestRecord.idealWeight = idealWeight;

        next();
    } catch (error) {
        next(error);
    }
});




userSchema.methods.matchPassword = async function (password) {
    return await bcrypt.compare(password, this.password);
};
export default mongoose.model('User', userSchema, 'users');
