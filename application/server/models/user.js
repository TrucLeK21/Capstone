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
        next();
    } catch (error) {
        next(error);
    }
});

userSchema.methods.matchPassword = async function (password) {
    return await bcrypt.compare(password, this.password);
};

userSchema.methods.addRecord = function({weight, height, dateOfBirth, gender, activityFactor}) {
    this.activityFactor = activityFactor;
    this.dateOfBirth = dateOfBirth;
    this.gender = gender;
    
    const date = new Date();
    const age = getAge(dateOfBirth);
    const bmi = getBmi(weight, height);
    const bmr = getBmr(weight, height, age, gender);
    const tdee = getTdee(weight, height, age, gender, activityFactor);
    const lbm = getLbm(weight, height, gender);
    const fatPercentage = getFatPercentage(weight, height, age, gender);
    const waterPercentage = getWaterPercentage(weight, height, age, gender);
    const boneMass = getBoneMass(weight, height, gender);
    const muscleMass = getMuscleMass(weight, height, age, gender);
    const proteinPercentage = getProteinPercentage(weight, height, age, gender);
    const visceralFat = getVisceralFat(weight, height, age, gender);
    const idealWeight = getIdealWeight(height, gender);

    const newRecord = {
        date, 
        height,
        weight,
        age,
        bmi,
        bmr,
        tdee,
        lbm,
        fatPercentage,
        waterPercentage,
        boneMass,
        muscleMass,
        proteinPercentage,
        visceralFat,
        idealWeight,
    }

    this.records.push(newRecord);
    return this.save();
}

function getAge(dateOfBirth) {
    const today = new Date();
    const birthDate = new Date(dateOfBirth);
    if (isNaN(birthDate) || birthDate > today) {
        return null;
    }

    let age = today.getFullYear() - birthDate.getFullYear();
    const isBirthdayPassed = (
        today.getMonth() > birthDate.getMonth() || 
        (today.getMonth() === birthDate.getMonth() && today.getDate() >= birthDate.getDate())
    );

    if (!isBirthdayPassed) {
        age--;
    }
    return age;
}

function getBmi(weight, height) {
    if (weight && height) {
        height = height / 100; // change to meter
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

function getTdee(weight, height, age, gender, activityFactor) {
    let bmr = getBmr(weight, height, age, gender);
    if(bmr) return parseFloat((bmr * activityFactor).toFixed(2));
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

function getProteinPercentage(weight, height, age, gender) {
    let muscleMass = getMuscleMass(weight, height, age, gender);
    let waterPercentage = getWaterPercentage(weight, height, age, gender);
    if(muscleMass && waterPercentage) return parseFloat(((muscleMass * 0.19 + weight * waterPercentage * 0.01 * 0.16) / weight * 100).toFixed(2));
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
