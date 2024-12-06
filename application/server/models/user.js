import mongoose from "mongoose";
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
    activityFactor: {
        type: Number,
        enum: [1.2, 1.375, 1.55, 1.725, 1.9],
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

}, {
    toObject: {
        transform: function (doc, ret) {
            delete ret._id; // Xóa trường _id
            return ret;
        }
    }
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

        // Calculate BMI based on height (cm) and weight (kg)
        const bmi = weightValue && heightInMeters
            ? parseFloat((weightValue / (heightInMeters ** 2)).toFixed(2))
            : null;
        // Calculate basal metabolic rate (BMR) and total daily energy expenditure (TDEE)
        let bmr = null;
        if (weightValue && heightValue && age !== null) {
            if (user.gender === 'male') {
                bmr = parseFloat((88.362 + (13.397 * weightValue) + (4.799 * heightValue) - (5.677 * age)).toFixed(2));
            } else if (user.gender === 'female') {
                bmr = parseFloat((447.593 + (9.247 * weightValue) + (3.098 * heightValue) - (4.330 * age)).toFixed(2));
            }
        }
        const tdee = bmr ? parseFloat((bmr * user.activityFactor).toFixed(2)) : null;

        //Calculate fat-free body mass (LBM)
        // const lbm = weightValue && heightValue
        //     ? parseFloat(((0.32810 * weightValue) + (0.33929 * heightValue) - 29.5336).toFixed(2))
        //     : null;
        let lbm = null;
        if (weightValue && heightValue) {
            if (user.gender === 'male') {
                lbm = parseFloat(((0.32810 * weightValue) + (0.33929 * heightValue) - 29.5336).toFixed(2));
            }
            else {
                lbm = parseFloat(((0.29569 * weightValue) + (0.41813 * heightValue) - 43.2933).toFixed(2));
            }
        }
        // Calculate body fat percentage
        // const fatPercentage = weightValue && lbm
        //     ? parseFloat((100 - (lbm / weightValue) * 100).toFixed(2))
        //     : null;
        let fatPercentage = null;
        if (weightValue && lbm) {
            fatPercentage = parseFloat(((1.20 * (weightValue - lbm) / weightValue * 100) + (0.23 * age) - (user.gender === 'male' ? 10.8 : 0) - 5.4).toFixed(2));
        }

        const waterPercentage = fatPercentage
            ? parseFloat(((100 - fatPercentage) * (user.gender === 'male' ? 0.55 : 0.49)).toFixed(2))
            : null;

        const boneMass = lbm
            ? parseFloat((lbm * (user.gender === 'male' ? 0.175 : 0.15)).toFixed(2))
            : null;

        const muscleMass = weightValue && fatPercentage && boneMass
            ? parseFloat((weightValue - (fatPercentage * 0.01 * weightValue) - boneMass).toFixed(2))
            : null;

        const proteinPercentage = muscleMass && weightValue && waterPercentage
            ? parseFloat(((muscleMass * 0.19 + weightValue * waterPercentage * 0.01 * 0.16) / weightValue * 100).toFixed(2))
            : null;

        // const visceralFat = age !== null
        //     ? parseFloat((1.0 + (age * 0.07)).toFixed(2))
        //     : null;

        const visceralFat = (age !== null && weightValue !== null && heightValue !== null)
            ? parseFloat(
                (
                    user.gender === 'male'
                        ? weightValue * 0.1 + age * 0.05 + (0.1 * (weightValue / heightValue))
                        : weightValue * 0.08 + age * 0.06 + (0.08 * (weightValue / heightValue))
                ).toFixed(2)
            )
            : null;


        // const idealWeight = heightValue
        //     ? parseFloat(((heightValue - 80) * 0.7).toFixed(2))
        //     : null;

        const idealWeight = heightValue !== null
            ? parseFloat(
                (
                    user.gender === 'male'
                        ? heightValue - 100 + (heightValue / 100)
                        : heightValue - 100 + ((heightValue / 100) * 0.9)
                ).toFixed(2)
            )
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

function getAge(dateOfBirth) {
    const today = new Date();
    if (dateOfBirth && !isNaN(new Date(dateOfBirth)) && new Date(dateOfBirth) <= today) {
        today.getFullYear() - new Date(dateOfBirth).getFullYear() - (
            ((today.getMonth() < new Date(user.dateOfBirth).getMonth() ||
                (today.getMonth() === new Date(user.dateOfBirth).getMonth() &&
                    today.getDate() < new Date(user.dateOfBirth).getDate())) ? 1 : 0)
        )
    }
    return null;
}
function getBmi(weight, height) {
    if (weight && height) {
        return parseFloat((weight / (height ** 2)).toFixed(2));
    }
    return null;
}

function getBmr(weight, height, age, gender) {
    if (weight && height && age && gender) {
        if (gender === 'male') {
            return parseFloat((88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)).toFixed(2));
        }
        else {
            return parseFloat((447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)).toFixed(2));
        }
    }
    return null;
}

function getLbm(weight, height, gender) {
    if (weight && height && gender) {
        if (gender === 'male') {
            return parseFloat(((0.32810 * weight) + (0.33929 * height) - 29.5336).toFixed(2));
        }
        else {
            return parseFloat(((0.29569 * weight) + (0.41813 * height) - 43.2933).toFixed(2));
        }
    }
    return null;
}

function getFatPercentage(weight, height, age, gender) {
    let lbm = getLbm(weight, height, gender);
    if (lbm) return parseFloat(((1.20 * (weight - lbm) / weight * 100) + (0.23 * age) - (gender === 'male' ? 10.8 : 0) - 5.4).toFixed(2));
    return null;
}

function getWaterPercentage(weight, height, age, gender) {
    let fatPercentage = getFatPercentage(weight, height, age, gender);
    if (fatPercentage) return parseFloat(((100 - fatPercentage) * (gender === 'male' ? 0.55 : 0.49)).toFixed(2));
    return null;
}

function getBoneMass(weight, height, gender) {
    let lbm = getLbm(weight, height, gender);
    if (lbm) return parseFloat((lbm * (gender === 'male' ? 0.175 : 0.15)).toFixed(2));
    return null;
}

function getMuscleMass(weight, height, age, gender) {
    let fatPercentage = getFatPercentage(weight, height, age, gender);
    let boneMass = getBoneMass(weight, height, gender);
    if (fatPercentage && boneMass) return parseFloat((weight - (fatPercentage * 0.01 * weight) - boneMass).toFixed(2));
    return null;
}

function getVisceralFat(weight, height, age, gender) {
    if (weight, height, age, gender) {
        return parseFloat(
            (
                gender === 'male'
                    ? weight * 0.1 + age * 0.05 + (0.1 * (weight / height))
                    : weight * 0.08 + age * 0.06 + (0.08 * (weight / height))
            ).toFixed(2)
        );
    }
    return null;
}

function getIdealWeight(height, gender) {
    if (height && gender) {
        return parseFloat(
            (
                gender === 'male'
                    ? height - 100 + (height / 100)
                    : height - 100 + ((height / 100) * 0.9)
            ).toFixed(2)
        );
    }
    return null;
}


export default mongoose.model('User', userSchema, 'users');
