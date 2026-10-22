# 🧪 โครงสร้างชุดทดสอบ (Tests Directory) - University Food Kcal
**มหาวิทยาลัยราชภัฏนครปฐม (NPRU)**

เอกสารและไฟล์ทดสอบทั้งหมดถูกจัดโครงสร้างตามมาตรฐานวิชาโครงงานระบบสารสนเทศ โดยมี 10 Test Cases หลักที่ครอบคลุมฟังก์ชันการทำงานจริงของระบบ:

---

## 📁 รายการไฟล์ทดสอบในโฟลเดอร์ `tests/`

| ไฟล์ทดสอบ | ฟังก์ชัน / วัตถุประสงค์การทดสอบ | Endpoint ที่เกี่ยวข้อง |
|---|---|---|
| `test_01_login.py` | ทดสอบการเข้าสู่ระบบสำเร็จ (Login Success) | `POST /api/auth/login` |
| `test_02_กรอกแบบฟอร์มและกดส่ง.py` | ทดสอบการกรอกแบบฟอร์มและกดส่งบันทึกมื้ออาหาร | `POST /api/logs` |
| `test_03_ติดตาม.py` | ทดสอบระบบติดตามแคลอรี่และสารอาหารประจำวัน | `GET /api/logs` & `GET /api/profile` |
| `test_04_login_ไม่ได้.py` | ทดสอบกรณีเข้าสู่ระบบไม่สำเร็จ (รหัสผ่านผิด / อีเมลผิด) | `POST /api/auth/login` |
| `test_05_กรอกฟอร์มผิด.py` | ทดสอบกรณีส่งฟอร์มข้อมูลไม่ครบ / ค่าผิดพลาด | `POST /api/logs` & `POST /api/foods` |
| `test_06_admin_แก้ไข.py` | ทดสอบผู้ดูแลระบบ (Admin) แก้ไขราคาและแคลอรี่อาหาร | `PUT /api/foods/:id` |
| `test_07_ลบ.py` | ทดสอบผู้ใช้ลบรายการอาหารที่บันทึกไว้ในบันทึกประจำวัน | `DELETE /api/logs/:id` |
| `test_08_กรอกติดตามผิด.py` | ทดสอบกรณีค้นหา/ติดตามข้อมูลผิดพลาด (404 Not Found) | `GET /api/foods/:id` & `GET /api/restaurants/:id` |
| `test_09_admin_ลบ.py` | ทดสอบผู้ดูแลระบบ (Admin) ลบเมนูอาหารออกจากฐานข้อมูล | `DELETE /api/foods/:id` |
| `test_10_admin_เปลี่ยน.py` | ทดสอบ Admin เปลี่ยนแปลงข้อมูลร้านค้าและตรวจสถิติระบบ | `PUT /api/restaurants/:id` & `GET /api/stats` |
| `test_portal_10_cases.py` | รวมการรันทั้ง 10 เคสต่อเนื่อง พร้อมสรุปตารางรายงานผล 100% | รวมทุก Endpoint |

---

## 🛠️ ไฟล์สนับสนุนในระบบการทดสอบ
* `helpers.py`: ตัวช่วยส่ง HTTP request (`ApiClient`) พร้อมระบบอ่าน/เขียน State
* `conftest.py`: การตั้งค่าและ Fixtures สำหรับรันผ่าน Pytest
* `run_tests.py`: สคริปต์หลักสำหรับสั่งรันชุดทดสอบทั้ง 10 เคส
* `requirements.txt`: ระบุไลบรารีที่จำเป็น (pytest, requests)
* `.test_state.json`: ไฟล์เก็บค่า Token, User ID และ State ส่งต่อระหว่างการทดสอบ

---

## 🚀 วิธีการสั่งรันการทดสอบ

### 1. รันรวมทุกเคส (10 Test Cases):
```bash
python tests/test_portal_10_cases.py
# หรือ
python tests/run_tests.py
```

### 2. รันแยกรายไฟล์เฉพาะเคสที่ต้องการ:
```bash
# ทดสอบ Login สำเร็จ
python tests/test_01_login.py

# ทดสอบกรอกฟอร์มบันทึกอาหาร
python "tests/test_02_กรอกแบบฟอร์มและกดส่ง.py"

# ทดสอบติดตามแคลอรี่
python "tests/test_03_ติดตาม.py"

# ทดสอบ Login ไม่ผ่าน
python "tests/test_04_login_ไม่ได้.py"

# ทดสอบ Admin แก้ไข
python "tests/test_06_admin_แก้ไข.py"

# ทดสอบลบรายการ
python "tests/test_07_ลบ.py"
```

### 3. รันผ่าน Pytest:
```bash
pytest tests/
```
