# University Food Kcal 🍱🔥

**เว็บแอปพลิเคชันสำหรับค้นหาและคำนวณแคลอรี่ (Kcal) ของอาหารภายในมหาวิทยาลัย**  
พัฒนาขึ้นเพื่อให้นักศึกษาและบุคลากรสามารถค้นหาเมนูอาหารในโรงอาหารมหาวิทยาลัย ตรวจสอบคุณค่าทางโภชนาการ (แคลอรี่, โปรตีน, คาร์โบไฮเดรต, ไขมัน) และคำนวณพลังงานรวมของมื้ออาหารได้อย่างถูกต้องและสะดวกสบาย

---

## 📌 โครงสร้างโปรเจกต์ (Project Structure)

```text
university-food-kcal/
├── backend/
│   ├── app.py                     # Flask Application & API Routes Setup
│   ├── requirements.txt           # Python Dependencies (Flask, PyMySQL, etc.)
│   ├── Dockerfile                 # Docker configuration for Flask Backend
│   ├── database/
│   │   └── schema.sql             # MySQL Schema & Seed Data (DDL + DML)
│   ├── routes/
│   │   ├── restaurant.py          # Flask REST API endpoints for Restaurants
│   │   └── food.py                # Flask REST API endpoints for Foods
│   └── models/
│       ├── restaurant.py          # Restaurant DB queries & Model methods
│       └── food.py                # Food DB queries & Model methods
│
├── src/
│   ├── components/
│   │   ├── Navbar.tsx             # Navigation bar with responsive menu
│   │   ├── FoodCard.tsx           # Food card with Kcal badge & nutrition info
│   │   └── FoodDetailModal.tsx    # Modal showing detailed macronutrients & energy ratio
│   ├── pages/
│   │   ├── HomePage.tsx           # Home page, search bar, and popular menus
│   │   ├── RestaurantsPage.tsx    # Campus restaurants list and restaurant food viewer
│   │   ├── FoodListPage.tsx       # Food list with search, filter (Kcal, price, store), and sorting
│   │   ├── CalculatorPage.tsx     # Calorie calculator with stepper, totals, and daily %
│   │   └── AdminDashboardPage.tsx # CRUD Management for restaurants and foods + Stats
│   ├── services/
│   │   └── api.ts                 # REST API client
│   ├── data/
│   │   └── initialData.ts         # Seed data (5 campus canteens & 17 university food items)
│   ├── types.ts                   # TypeScript interfaces
│   ├── App.tsx                    # Main React Application
│   ├── main.tsx                   # React DOM render entry point
│   └── index.css                  # Global Tailwind CSS
│
├── server.ts                      # Full-stack server (Express + Vite + REST API & persistence)
├── nginx.conf                     # Nginx proxy configuration for Docker container
├── Dockerfile                     # Multi-stage Dockerfile for React frontend
├── docker-compose.yml             # Docker Compose orchestration (MySQL + Flask + React)
├── metadata.json                  # Application metadata
├── package.json                   # Node.js dependencies and scripts
└── README.md                      # Complete project documentation
```

---

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)

- **Frontend**: React 19, Vite, Tailwind CSS, Lucide React, Google Font (Prompt)
- **Backend**: Python 3.10+, Flask, Flask-CORS, PyMySQL, SQLAlchemy
- **Database**: MySQL 8.0 (Database name: `university_food_kcal`)
- **API Standard**: RESTful API (JSON)
- **Containerization**: Docker, Docker Compose, Nginx

---

## 🗄️ โครงสร้างฐานข้อมูล (Database Schema)

ฐานข้อมูลชื่อ: `university_food_kcal` ประกอบด้วย 2 ตารางหลัก พร้อม Foreign Key:

### 1. ตาราง `restaurants` (ร้านอาหาร)
| Column | Type | Description |
|---|---|---|
| `id` | INT (PK, Auto Increment) | รหัสร้านอาหาร |
| `name` | VARCHAR(255) NOT NULL | ชื่อร้านอาหาร |
| `description` | TEXT | รายละเอียดร้านอาหาร |
| `location` | VARCHAR(255) NOT NULL | ตำแหน่ง/สถานที่ตั้ง (เช่น โรงอาหารกลาง 1) |
| `image` | VARCHAR(500) | ลิงก์รูปภาพร้านค้า |
| `phone` | VARCHAR(50) | เบอร์ติดต่อ |
| `open_hours` | VARCHAR(100) | เวลาเปิด-ปิด |
| `created_at` | TIMESTAMP | วันเวลาที่สร้างข้อมูล |

### 2. ตาราง `foods` (เมนูอาหาร)
| Column | Type | Description |
|---|---|---|
| `id` | INT (PK, Auto Increment) | รหัสอาหาร |
| `name` | VARCHAR(255) NOT NULL | ชื่อเมนูอาหาร |
| `restaurant_id` | INT (FK) | รหัสร้านค้า (เชื่อมกับ `restaurants.id`) |
| `price` | DECIMAL(10,2) | ราคา (บาท) |
| `kcal` | INT NOT NULL | พลังงาน (กิโลแคลอรี่) |
| `protein` | DECIMAL(6,1) | โปรตีน (กรัม) |
| `carbohydrate` | DECIMAL(6,1) | คาร์โบไฮเดรต (กรัม) |
| `fat` | DECIMAL(6,1) | ไขมัน (กรัม) |
| `image` | VARCHAR(500) | ลิงก์รูปภาพอาหาร |
| `description` | TEXT | รายละเอียดอาหาร |
| `category` | VARCHAR(100) | หมวดหมู่อาหาร |
| `is_popular` | BOOLEAN | สถานะเมนูยอดนิยม (True/False) |
| `created_at` | TIMESTAMP | วันเวลาที่สร้างข้อมูล |

---

## 📡 ระบบ REST API (Backend Endpoints)

### ร้านอาหาร (Restaurants API)
- `GET /api/restaurants` — ดึงข้อมูลร้านอาหารทั้งหมด
- `GET /api/restaurants/<id>` — ดึงข้อมูลร้านอาหารตาม ID
- `POST /api/restaurants` — เพิ่มร้านอาหารใหม่
- `PUT /api/restaurants/<id>` — แก้ไขข้อมูลร้านอาหาร
- `DELETE /api/restaurants/<id>` — ลบร้านอาหาร (และลบเมนูอาหารในร้านอัตโนมัติด้วย CASCADE)

### เมนูอาหาร (Foods API)
- `GET /api/foods` — ดึงรายการอาหาร (รองรับ Query: `search`, `restaurant_id`, `min_kcal`, `max_kcal`, `sort_by`)
- `GET /api/foods/<id>` — ดึงข้อมูลเมนูอาหารตาม ID
- `GET /api/foods/restaurant/<restaurant_id>` — ดึงเมนูอาหารเฉพาะของร้านที่ระบุ
- `POST /api/foods` — เพิ่มเมนูอาหารใหม่
- `PUT /api/foods/<id>` — แก้ไขข้อมูลเมนูอาหาร
- `DELETE /api/foods/<id>` — ลบเมนูอาหาร

### สถิติและระบบ (Stats API)
- `GET /api/stats` — สรุปสถิติจำนวนร้าน, จำนวนเมนู, ค่าเฉลี่ย Kcal, เมนู Kcal สูงสุด/ต่ำสุด
- `GET /api/health` — ตรวจสอบสถานะการทำงานของระบบ API

---

## 🚀 วิธีการติดตั้งและรันโปรเจกต์ (How to Run)

### วิธีที่ 1: รันด้วย Docker Compose (แนะนำ สะดวกที่สุด)

ระบบจะเปิด container 3 ตัวพร้อมกัน ได้แก่:
1. `db`: MySQL 8.0 พร้อมโหลดไฟล์ `schema.sql` และข้อมูลเริ่มต้นอัตโนมัติ
2. `backend`: Python Flask REST API ทำงานบนพอร์ต 5000
3. `frontend`: React Vite ทำงานบนพอร์ต 3000

```bash
# 1. โคลนโปรเจกต์
git clone https://github.com/thaptawon123/project4.git
cd university-food-kcal

# 2. เริ่มต้นระบบทั้งหมดด้วย Docker Compose
docker-compose up --build

# 3. เปิดเบราว์เซอร์เข้าใช้งาน
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000/api/health
```

---

### วิธีที่ 2: รันแบบ Manual (Local Development)

#### 1. เตรียมฐานข้อมูล MySQL
- เปิดโปรแกรม MySQL (เช่น phpMyAdmin หรือ MySQL Workbench)
- สร้างฐานข้อมูลและนำเข้าไฟล์ SQL:
```bash
mysql -u root -p < backend/database/schema.sql
```

#### 2. รัน Flask Backend
```bash
cd backend
python -m venv venv

# บน Windows:
venv\Scripts\activate
# บน macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python app.py
# Backend ทำงานที่ http://localhost:5000
```

#### 3. รัน React Frontend
```bash
# เปิด Terminal ใหม่ที่ root directory
npm install
npm run dev
# Frontend ทำงานที่ http://localhost:3000
```

---

## 🌟 ฟังก์ชันหลักของระบบ (Key Features)

1. **หน้า Home**:
   - ค้นหาอาหารหรือร้านค้าได้ทันที
   - แนะนำเมนูยอดนิยมพร้อมแสดง Kcal ชัดเจน
   - หมวดหมู่คัดลอกด่วน (อาหารจานเดียว, ก๋วยเตี๋ยว, อาหารเพื่อสุขภาพ, เครื่องดื่ม)

2. **ระบบร้านอาหาร (Restaurants)**:
   - แสดงรายชื่อร้านค้าในโรงอาหารมหาวิทยาลัย
   - แสดงตำแหน่งที่ตั้ง เวลาเปิด-ปิด และเบอร์ติดต่อ
   - กดดูรายละเอียดและเมนูทั้งหมดของแต่ละร้านได้ทันที

3. **ระบบเมนูอาหาร (Food List)**:
   - ค้นหาตามชื่ออาหาร
   - กรองตามร้านค้า, ช่วง Kcal (< 300, 300-500, 500-700, > 700), และระดับราคา
   - จัดเรียงตาม Kcal ต่ำไปสูง, สูงไปต่ำ หรือราคา

4. **ระบบคำนวณ Kcal (Food Calculator)**:
   - เพิ่มอาหารเข้าสู่รายการคำนวณ
   - ปรับจำนวนจาน (+/-) หรือลบรายการ
   - คำนวณ **Kcal รวม, โปรตีนรวม, คาร์โบไฮเดรตรวม และไขมันรวม** แบบ Real-time
   - แสดงแถบเทียบกับความต้องการพลังงานต่อวัน (~2,000 Kcal)
   - ฟังก์ชันคัดลอกสรุปรายการอาหาร (Share / Copy Summary)

5. **หน้ารายละเอียดอาหาร (Food Detail)**:
   - แสดงภาพอาหารขนาดใหญ่ ข้อมูลร้าน ราคา และพลังงาน Kcal
   - แถบสัดส่วนสารอาหาร Macronutrients (Protein / Carb / Fat)
   - ปรับจำนวนและกดเพิ่มเข้ารายการคำนวณได้ทันที

6. **แดชบอร์ดผู้ดูแล (Admin Dashboard)**:
   - สรุปสถิติภาพรวม: จำนวนร้าน, จำนวนเมนู, ค่าเฉลี่ย Kcal, เมนู Kcal สูงสุด/ต่ำสุด
   - จัดการร้านอาหาร (CRUD: เพิ่ม, แก้ไข, ลบ)
   - จัดการเมนูอาหาร (CRUD: เพิ่ม, แก้ไข, ลบ)
   - ปุ่มรีเซ็ตข้อมูลตัวอย่างกลับเป็นค่าเริ่มต้น (Reset Seed Data)
