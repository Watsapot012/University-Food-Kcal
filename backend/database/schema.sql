-- ==========================================================
-- Database Schema for University Food Kcal
-- ==========================================================

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS university_food_kcal 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE university_food_kcal;

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 1. Table: restaurants
DROP TABLE IF EXISTS meal_logs;
DROP TABLE IF EXISTS profiles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS foods;
DROP TABLE IF EXISTS restaurants;

CREATE TABLE restaurants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255) NOT NULL,
    image VARCHAR(500),
    phone VARCHAR(50) DEFAULT NULL,
    open_hours VARCHAR(100) DEFAULT '08:00 - 18:00 น.',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Table: foods
CREATE TABLE foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    restaurant_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    kcal INT NOT NULL DEFAULT 0,
    protein DECIMAL(6,1) NOT NULL DEFAULT 0.0,
    carbohydrate DECIMAL(6,1) NOT NULL DEFAULT 0.0,
    fat DECIMAL(6,1) NOT NULL DEFAULT 0.0,
    image VARCHAR(500),
    description TEXT,
    category VARCHAR(100) DEFAULT 'อาหารจานเดียว',
    is_popular BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_foods_restaurant 
        FOREIGN KEY (restaurant_id) 
        REFERENCES restaurants(id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Table: users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    avatar VARCHAR(500),
    role VARCHAR(50) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Table: profiles
CREATE TABLE profiles (
    user_id INT PRIMARY KEY,
    weight DECIMAL(5,2) DEFAULT 65.0,
    height DECIMAL(5,2) DEFAULT 175.0,
    age INT DEFAULT 21,
    gender VARCHAR(10) DEFAULT 'male',
    activity DECIMAL(4,3) DEFAULT 1.55,
    bmr INT DEFAULT 1650,
    tdee INT DEFAULT 2558,
    calories INT DEFAULT 2000,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_profiles_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Table: meal_logs
CREATE TABLE meal_logs (
    id VARCHAR(100) PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    calories INT NOT NULL DEFAULT 0,
    type VARCHAR(50) DEFAULT 'lunch',
    timestamp VARCHAR(50),
    protein DECIMAL(6,1) DEFAULT 0.0,
    carbs DECIMAL(6,1) DEFAULT 0.0,
    fat DECIMAL(6,1) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_meal_logs_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==========================================================
-- Seed Data: Sample University Canteens & Restaurants
-- ==========================================================

INSERT INTO restaurants (id, name, description, location, image, phone, open_hours) VALUES
(1, 'ร้านป้าณี ตามสั่งตามใจ', 'อาหารจานด่วน ผัดกะเพรา ข้าวผัด อาหารตามสั่งรสจัดจ้าน ปรุงสุกใหม่กระทะต่อกระทะ', 'โรงอาหารกลาง 1 (Canteen 1) ล็อค 04', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80', '081-234-5678', '08:00 - 18:00 น.'),
(2, 'ข้าวมันไก่เฮียชัย โกเบ', 'ข้าวมันไก่ตอนเนื้อนุ่ม หนังกรอบ น้ำจิ้มเต้าเจี้ยวสูตรเด็ด พร้อมน้ำซุปกระดูกไก่ร้อนๆ', 'โรงอาหารกลาง 1 (Canteen 1) ล็อค 09', 'https://images.unsplash.com/photo-1569058242253-92a9c755a0ec?auto=format&fit=crop&w=800&q=80', '082-345-6789', '07:30 - 15:00 น.'),
(3, 'ก๋วยเตี๋ยวเรือมหาลัย แซ่บถึงใจ', 'ก๋วยเตี๋ยวน้ำตกสูตรเข้มข้น ก๋วยเตี๋ยวต้มยำหมูสับมะนาวแท้ หมูนุ่ม ลูกชิ้นปลาสด', 'โรงอาหารหอพักนักศึกษา (Dorm Canteen) ล็อค 02', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=80', '083-456-7890', '09:00 - 20:00 น.'),
(4, 'Green & Fit สลัดและสเต็กเด็กมอ', 'เมนูสุขภาพสำหรับสายฟิต อกไก่ย่าง สลัดผักไฮโดรโปนิกส์ และสเต็กโปรตีนสูง', 'อาคารกิจกรรมนักศึกษา ชั้น 1', 'https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80', '084-567-8901', '10:00 - 19:30 น.'),
(5, 'ซุ้มเครื่องดื่ม & ขนมหวาน UniChill', 'ชาไทย ชาเขียว กาแฟสด น้ำผลไม้ปั่น และเครื่องดื่มสุขภาพหวานน้อย', 'ลานกิจกรรมหน้าหอสมุดกลาง', 'https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=800&q=80', '085-678-9012', '07:00 - 18:30 น.');

-- ==========================================================
-- Seed Data: Sample Foods
-- ==========================================================

INSERT INTO foods (id, name, restaurant_id, price, kcal, protein, carbohydrate, fat, image, description, category, is_popular) VALUES
(1, 'ข้าวกะเพราไก่ + ไข่ดาว', 1, 50.00, 590, 28.0, 55.0, 26.0, 'https://images.unsplash.com/photo-1569058242253-92a9c755a0ec?auto=format&fit=crop&w=800&q=80', 'ผัดกะเพราไก่สับพริกแห้งหอมกรุ่น เสิร์ฟคู่ข้าวสวยร้อนๆ และไข่ดาวทอดกรอบ', 'อาหารจานเดียว', TRUE),
(2, 'ข้าวมันไก่ตอน (เนื้อน่องไม่เอาหนัง)', 2, 45.00, 520, 27.0, 65.0, 16.0, 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=800&q=80', 'ข้าวมันหอมนุ่ม ไก่ตอนต้มสุกกำลังดี เสิร์ฟพร้อมน้ำจิ้มขิงเต้าเจี้ยวรสจัดจ้านและแตงกวา', 'อาหารจานเดียว', TRUE),
(3, 'ข้าวมันไก่ตอนพิเศษ (เนื้อน่องติดหนัง)', 2, 55.00, 640, 29.0, 70.0, 26.0, 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=800&q=80', 'ข้าวมันไก่จานพิเศษ เพิ่มเนื้อไก่และข้าว อิ่มจุใจสำหรับมื้อกลางวัน', 'อาหารจานเดียว', FALSE),
(4, 'ข้าวหมูกรอบคั่วพริกเกลือ', 1, 60.00, 680, 20.0, 58.0, 40.0, 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80', 'หมูกรอบเนื้อแน่นทอดกรอบ คั่วพริกกระเทียมเกลือรสเข้มข้น รสชาติจัดจ้านสะใจ', 'อาหารจานเดียว', TRUE),
(5, 'ข้าวผัดกุ้งสด', 1, 55.00, 530, 20.0, 65.0, 18.0, 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=800&q=80', 'ข้าวสวยผัดไข่ใส่กุ้งขาวสด เม็ดข้าวร่วนสวย กลิ่นหอมกระทะ เสิร์ฟพร้อมมะนาวและต้นหอม', 'อาหารจานเดียว', FALSE),
(6, 'ข้าวไข่เจียวทรงเครื่องหมูสับ', 1, 40.00, 610, 19.0, 52.0, 35.0, 'https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?auto=format&fit=crop&w=800&q=80', 'ไข่เจียว 2 ฟองตีฟูใส่หมูสับและหอมใหญ่ ทอดสีเหลืองทองกรอบนอกนุ่มใน', 'อาหารจานเดียว', FALSE),
(7, 'ก๋วยเตี๋ยวต้มยำหมูสับมะนาวสด', 3, 45.00, 340, 20.0, 46.0, 8.0, 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=80', 'เส้นเล็กต้มยำสูตรพริกเผามะนาวแท้ ใส่หมูสับ หมูชิ้น ลูกชิ้นปลา และถั่วลิสงคั่วบดใหม่', 'ก๋วยเตี๋ยว', TRUE),
(8, 'ก๋วยเตี๋ยวเรือหมูน้ำตกเข้มข้น', 3, 45.00, 360, 22.0, 45.0, 9.0, 'https://images.unsplash.com/photo-1552611052-33e04de081de?auto=format&fit=crop&w=800&q=80', 'น้ำซุปกระดูกหมูตุ๋นสมุนไพรจีนรสกลมกล่อม หมูนุ่ม ตับลวก และผักบุ้งกรอบ', 'ก๋วยเตี๋ยว', TRUE),
(9, 'สุกี้น้ำรวมมิตรทะเลและหมู', 3, 50.00, 280, 23.0, 28.0, 6.0, 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=80', 'เมนูแคลอรี่ต่ำ ผักกาดขาว วุ้นเส้น อกหมู กุ้ง และไข่ไก่ ราดน้ำจิ้มสุกี้เต้าหู้ยี้รสเด็ด', 'อาหารเพื่อสุขภาพ', TRUE),
(10, 'สลัดอกไก่ย่างน้ำสลัดงาญี่ปุ่น', 4, 59.00, 290, 32.0, 14.0, 10.0, 'https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80', 'อกไก่หมักพริกไทยดำย่างหอมกรุ่น เสิร์ฟคู่ผักไฮโดร คอร์น มะเขือเทศราชินี และน้ำสลัดงาคั่วญี่ปุ่น', 'อาหารเพื่อสุขภาพ', TRUE),
(11, 'สเต็กอกไก่สไปซี่พร้อมขนมปังกระเทียม', 4, 69.00, 390, 36.0, 20.0, 16.0, 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=800&q=80', 'อกไก่ชิ้นโตหมักซอสสไปซี่ ย่างฉ่ำเนื้อนุ่ม เสิร์ฟพร้อมสลัดผักและขนมปังกระเทียม', 'สเต็กและโปรตีน', FALSE),
(12, 'ยำวุ้นเส้นหมูสับกุ้งสด', 1, 50.00, 220, 18.0, 30.0, 3.0, 'https://images.unsplash.com/photo-1569058242253-92a9c755a0ec?auto=format&fit=crop&w=800&q=80', 'ยำวุ้นเส้นรสแซ่บ เปรี้ยว เผ็ด เค็ม ครบรส ใส่หมูสับ กุ้งสด เห็ดหูหนูขาว และคื่นช่าย แคลอรี่ต่ำมาก', 'อาหารเพื่อสุขภาพ', TRUE),
(13, 'ผัดซีอิ๊วเส้นใหญ่หมูนุ่ม', 1, 50.00, 580, 22.0, 60.0, 26.0, 'https://images.unsplash.com/photo-1555126634-323283e090fa?auto=format&fit=crop&w=800&q=80', 'เส้นใหญ่ผัดซีอิ๊วดำหอมกลิ่นคั่วกระทะ ใส่หมูหมักนุ่ม ไข่ไก่ และคะน้าฮ่องกงกรอบ', 'อาหารจานเดียว', FALSE),
(14, 'ไข่ดาวฟองทอดกรอบ (Add-on)', 1, 10.00, 160, 7.0, 1.0, 14.0, 'https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=800&q=80', 'ไข่ดาวทอดขอบกรอบ ไข่แดงเยิ้ม เพิ่มพลังงานและโปรตีนให้มื้ออาหาร', 'ของทานเล่น/เครื่องเคียง', FALSE),
(15, 'ชาไทยเย็นหวานน้อย (25%)', 5, 30.00, 160, 3.0, 24.0, 6.0, 'https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=800&q=80', 'ชาไทยแท้ชงสด ชาหอมเข้มข้น ผสมนมสดหวานน้อย สดชื่นระหว่างเรียน', 'เครื่องดื่ม', TRUE),
(16, 'ชาเขียวมัทฉะนมสดเย็น', 5, 35.00, 140, 4.0, 20.0, 5.0, 'https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=800&q=80', 'มัทฉะแท้เกรดพรีเมียมตีกับนมสดพร่องมันเนย หอมมัน กลมกล่อม', 'เครื่องดื่ม', FALSE),
(17, 'น้ำดื่มบริสุทธิ์ตรามหาวิทยาลัย (600 ml)', 5, 10.00, 0, 0.0, 0.0, 0.0, 'https://images.unsplash.com/photo-1548839140-29a749e1bc4e?auto=format&fit=crop&w=800&q=80', 'น้ำดื่มสะอาดผ่านระบบกรอง RO ปราศจากแคลอรี่ คืนความสดชื่น 100%', 'เครื่องดื่ม', FALSE),
(18, 'ข้าวกะเพราหมูกรอบสูตรพริกแห้ง', 1, 60.00, 720, 23.0, 68.0, 39.0, 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80', 'หมูกรอบชิ้นโตทอดกรอบ ผัดกะเพราพริกแห้งใบกะเพราบ้านหอมฉุน เผ็ดร้อนจัดจ้าน ขวัญใจเด็กมอ', 'อาหารจานเดียว', TRUE),
(19, 'ข้าวกะเพราหมูสับไข่ดาวไม่สุก', 1, 50.00, 620, 27.0, 56.0, 28.0, 'https://images.unsplash.com/photo-1569058242253-92a9c755a0ec?auto=format&fit=crop&w=800&q=80', 'กะเพราหมูสับคั่วแห้งสไตล์โบราณ เสิร์ฟพร้อมไข่ดาวทอดกรอบไข่แดงเยิ้ม รสชาติกลมกล่อม', 'อาหารจานเดียว', TRUE),
(20, 'ข้าวกะเพราอกไก่คลีน (ผัดน้ำไม่ใช้น้ำมัน)', 4, 55.00, 380, 39.0, 48.0, 4.0, 'https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80', 'เมนูยอดฮิตสายสุขภาพ อกไก่นุ่มผัดกะเพราด้วยน้ำซุปสมุนไพร ไม่ใช้น้ำมัน โซเดียมต่ำ โปรตีนสูง', 'อาหารเพื่อสุขภาพ', TRUE),
(21, 'ข้าวกะเพราทะเลรวมมิตร (กุ้ง+หมึกสด)', 1, 65.00, 480, 32.0, 58.0, 12.0, 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=80', 'กุ้งสดตัวโตและปลาหมึกชิ้นเด้ง ผัดใบกะเพราสดรสชาติจัดจ้าน หอมกลิ่นกระทะ เสิร์ฟร้อนๆ', 'อาหารจานเดียว', TRUE),
(22, 'ข้าวกะเพราเนื้อสับพริกสด', 1, 65.00, 660, 33.0, 55.0, 31.0, 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80', 'เนื้อวัวบดผัดกะเพราพริกขี้หนูสวนสด เผ็ดแซ่บสะใจ หอมใบกะเพราคั่วไฟแรง', 'อาหารจานเดียว', FALSE),
(23, 'ข้าวกะเพราเต้าหู้เห็ดหอม (มังสวิรัติ)', 4, 45.00, 390, 18.0, 60.0, 8.0, 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80', 'เต้าหู้ขาวทอดเนื้อนุ่มและเห็ดหอม ผัดใบกะเพราซอสเห็ดหอมรสเข้มข้น แคลอรี่เบาๆ สุขภาพดี', 'อาหารเพื่อสุขภาพ', FALSE);

-- ==========================================================
-- Seed Data: Sample User & Profile
-- ==========================================================

INSERT INTO users (id, name, email, password_hash, avatar, role) VALUES
(1, 'นักศึกษาสุขภาพดี', 'student@npru.ac.th', 'password123', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80', 'student');

INSERT INTO profiles (user_id, weight, height, age, gender, activity, bmr, tdee, calories) VALUES
(1, 65.0, 175.0, 21, 'male', 1.55, 1650, 2558, 2000);

INSERT INTO meal_logs (id, user_id, name, calories, type, timestamp, protein, carbs, fat) VALUES
('log-1', 1, 'ข้าวกะเพราไก่ + ไข่ดาว', 590, 'lunch', '12:30 น.', 28.0, 55.0, 26.0),
('log-2', 1, 'ชาไทยเย็นหวานน้อย (25%)', 160, 'snack', '14:15 น.', 3.0, 24.0, 6.0);
