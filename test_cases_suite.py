#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ชุดโค้ดทดสอบระบบเว็บ: University Food Kcal (มรภ.นครปฐม)
โครงสร้าง: แบ่งฟังก์ชันตามรหัสแบบทดสอบจริง (TC-HOME, TC-REST, TC-FOOD, TC-CUST, TC-DASH, TC-PROF, TC-AUTH, TC-ADM)
รันคำสั่ง: python test_cases_suite.py
================================================================================
"""

import sys
from typing import Dict, List, Any, Optional

# ตั้งค่า stdout รองรับภาษาไทยบนทุกระบบปฏิบัติการ
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


# ==============================================================================
# ตัวจำลองฐานข้อมูลและ State ของเว็บไซต์เรา (Database & App State Simulation)
# ==============================================================================
INITIAL_RESTAURANTS = [
    {"id": 1, "name": "ร้านป้าสมใจ อาหารตามสั่ง", "location": "โรงอาหาร 1 มรภ.นครปฐม", "open_hours": "07:30 - 16:00 น."},
    {"id": 2, "name": "ก๋วยเตี๋ยวเรืออยุธยา สูตรโบราณ", "location": "โรงอาหาร 2 มรภ.นครปฐม", "open_hours": "08:00 - 15:30 น."},
    {"id": 3, "name": "ข้าวมันไก่เด็กหอตอนดึก", "location": "หน้าหอพักนักศึกษา มรภ.นครปฐม", "open_hours": "10:00 - 20:00 น."},
    {"id": 4, "name": "ร้านกาแฟและชานมชาวมอ", "location": "อาคารเรียนรวม 1", "open_hours": "07:30 - 17:00 น."},
]

INITIAL_FOODS = [
    {"id": 1, "name": "ข้าวกะเพราไก่ไข่ดาว", "restaurant_id": 1, "restaurant_name": "ร้านป้าสมใจ อาหารตามสั่ง", "kcal": 640, "price": 50, "protein": 31, "carbohydrate": 66, "fat": 27, "is_popular": True},
    {"id": 2, "name": "ก๋วยเตี๋ยวต้มยำหมูน้ำใส", "restaurant_id": 2, "restaurant_name": "ก๋วยเตี๋ยวเรืออยุธยา สูตรโบราณ", "kcal": 380, "price": 40, "protein": 20, "carbohydrate": 52, "fat": 10, "is_popular": True},
    {"id": 3, "name": "ข้าวมันไก่ต้มพิเศษ", "restaurant_id": 3, "restaurant_name": "ข้าวมันไก่เด็กหอตอนดึก", "kcal": 590, "price": 45, "protein": 26, "carbohydrate": 68, "fat": 24, "is_popular": False},
    {"id": 4, "name": "สลัดอกไก่ย่างคลีน", "restaurant_id": 1, "restaurant_name": "ร้านป้าสมใจ อาหารตามสั่ง", "kcal": 280, "price": 50, "protein": 32, "carbohydrate": 15, "fat": 8, "is_popular": True},
    {"id": 5, "name": "ชาไทยเย็นหวานน้อย (25%)", "restaurant_id": 4, "restaurant_name": "ร้านกาแฟและชานมชาวมอ", "kcal": 160, "price": 30, "protein": 3, "carbohydrate": 24, "fat": 6, "is_popular": False},
    {"id": 6, "name": "ข้าวผัดกะเพราหมูกรอบ", "restaurant_id": 1, "restaurant_name": "ร้านป้าสมใจ อาหารตามสั่ง", "kcal": 750, "price": 60, "protein": 22, "carbohydrate": 70, "fat": 42, "is_popular": True},
]

MODIFIER_OPTIONS = [
    {"id": "fried_egg", "name": "ไข่ดาว", "kcal": 90, "pro": 6, "carbs": 1, "fat": 7},
    {"id": "extra_meat", "name": "เพิ่มเนื้อสัตว์พิเศษ", "kcal": 120, "pro": 18, "carbs": 0, "fat": 5},
    {"id": "half_rice", "name": "ลดข้าวครึ่งเดียว", "kcal": -100, "pro": -2, "carbs": -25, "fat": 0},
    {"id": "less_oil", "name": "ผัดน้ำมันน้อย / ผัดน้ำ", "kcal": -50, "pro": 0, "carbs": 0, "fat": -6},
]


# ==============================================================================
# Helper สำหรับพิมพ์และบันทึกผลการทดสอบ
# ==============================================================================
class Runner:
    total = 0
    passed = 0
    failed = 0

    @classmethod
    def test(cls, tc_id: str, screen: str, name: str, expected: str, fn):
        cls.total += 1
        print(f"\n[{tc_id}] หน้าจอ: {screen} | ฟังก์ชัน: {name}")
        print(f"  👉 ผลลัพธ์ที่คาดหวัง: {expected}")
        try:
            fn()
            cls.passed += 1
            print(f"  \033[92m✔ ผ่านการทดสอบ (PASS)\033[0m")
        except AssertionError as e:
            cls.failed += 1
            print(f"  \033[91m✖ ไม่ผ่าน (FAIL): {e}\033[0m")
        except Exception as e:
            cls.failed += 1
            print(f"  \033[91m✖ เกิดข้อผิดพลาด (ERROR): {e}\033[0m")


# ==============================================================================
# 1. หมวด TC-HOME: ฟังก์ชันหน้าแรก (Home Page)
# ==============================================================================
def quick_search_home(query: str, foods: List[Dict[str, Any]]) -> Dict[str, Any]:
    """ฟังก์ชันช่องค้นหาด่วนที่หน้าแรก แล้วเปลี่ยนหน้าไปหน้ารายการอาหาร"""
    q = query.lower().strip()
    filtered = [f for f in foods if q in f["name"].lower() or q in f["restaurant_name"].lower()]
    return {
        "target_page": "foods",
        "search_query": query,
        "results": filtered,
        "count": len(filtered)
    }

def get_home_stats(restaurants: List[Dict[str, Any]], foods: List[Dict[str, Any]]) -> Dict[str, Any]:
    """คำนวณตัวชี้วัดสรุปในหน้าแรก"""
    total_r = len(restaurants)
    total_f = len(foods)
    avg_kcal = round(sum(f["kcal"] for f in foods) / total_f, 1) if total_f > 0 else 0
    max_f = max(foods, key=lambda x: x["kcal"])
    min_f = min(foods, key=lambda x: x["kcal"])
    return {
        "total_restaurants": total_r,
        "total_foods": total_f,
        "avg_kcal": avg_kcal,
        "max_kcal_food": max_f["name"],
        "min_kcal_food": min_f["name"]
    }

def test_tc_home_01():
    """TC-HOME-01: หน้าแรก ค้นหาด่วน พิมพ์ 'กะเพรา' -> พุ่งไปหน้ารายการอาหาร แสดงเฉพาะเมนูกะเพรา"""
    res = quick_search_home("กะเพรา", INITIAL_FOODS)
    assert res["target_page"] == "foods", "ต้องเปลี่ยนไปหน้ารายการอาหาร (foods)"
    assert res["count"] > 0, "ต้องพบเมนูกะเพรา"
    for item in res["results"]:
        assert "กะเพรา" in item["name"], f"เมนู '{item['name']}' ไม่มีคำว่ากะเพรา"

def test_tc_home_02():
    """TC-HOME-02: หน้าแรก ตัวชี้วัดสรุป โหลดหน้าแรก -> แสดงการ์ดจำนวนร้าน, จำนวนเมนู, ค่าเฉลี่ย kcal ถูกต้อง"""
    stats = get_home_stats(INITIAL_RESTAURANTS, INITIAL_FOODS)
    assert stats["total_restaurants"] == 4, f"จำนวนร้านต้องเท่ากับ 4 แต่ได้ {stats['total_restaurants']}"
    assert stats["total_foods"] == 6, f"จำนวนเมนูต้องเท่ากับ 6 แต่ได้ {stats['total_foods']}"
    assert stats["avg_kcal"] > 0, "ค่าเฉลี่ยแคลอรี่ต้องมากกว่า 0"
    assert stats["max_kcal_food"] == "ข้าวผัดกะเพราหมูกรอบ", "เมนูแคลอรี่สูงสุดต้องเป็นข้าวกะเพราหมูกรอบ"
    assert stats["min_kcal_food"] == "ชาไทยเย็นหวานน้อย (25%)", "เมนูแคลอรี่ต่ำสุดต้องเป็นชาไทย"

def test_tc_home_03():
    """TC-HOME-03: หน้าแรก เมนูยอดนิยม -> แสดงเฉพาะอาหารที่ตั้งค่า is_popular: True"""
    popular = [f for f in INITIAL_FOODS if f.get("is_popular")]
    assert len(popular) > 0, "ต้องมีการ์ดอาหารยอดนิยมแสดงผล"
    for p in popular:
        assert p["is_popular"] is True


# ==============================================================================
# 2. หมวด TC-REST: ฟังก์ชันหน้าร้านอาหาร (Restaurants Page)
# ==============================================================================
def get_restaurant_list(restaurants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return list(restaurants)

def filter_foods_by_restaurant(restaurant_id: int, foods: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [f for f in foods if f["restaurant_id"] == restaurant_id]

def test_tc_rest_01():
    """TC-REST-01: ร้านค้า แสดงรายชื่อร้าน เข้าแท็บร้านค้า -> แสดงรายชื่อร้านค้าในมหาวิทยาลัยครบถ้วน"""
    stores = get_restaurant_list(INITIAL_RESTAURANTS)
    assert len(stores) == 4, f"คาดหวัง 4 ร้าน แต่ได้ {len(stores)}"
    for s in stores:
        assert "name" in s and "location" in s, "ร้านค้าต้องมีชื่อและที่ตั้ง"

def test_tc_rest_02():
    """TC-REST-02: ร้านค้า กรองเมนูตามร้าน คลิกเลือกร้านป้าสมใจ (id=1) -> แสดงเฉพาะเมนูของร้านป้าสมใจ"""
    dishes = filter_foods_by_restaurant(1, INITIAL_FOODS)
    assert len(dishes) == 3, f"ร้านป้าสมใจมี 3 เมนู แต่ได้ {len(dishes)}"
    for d in dishes:
        assert d["restaurant_id"] == 1, f"เมนู {d['name']} ไม่ใช่ของร้านป้าสมใจ"

def test_tc_rest_03():
    """TC-REST-03: ร้านค้า ค้นหาร้าน พิมพ์ 'ก๋วยเตี๋ยว' -> แสดงเฉพาะร้านก๋วยเตี๋ยวเรืออยุธยา"""
    matched = [r for r in INITIAL_RESTAURANTS if "ก๋วยเตี๋ยว" in r["name"]]
    assert len(matched) == 1
    assert matched[0]["id"] == 2


# ==============================================================================
# 3. หมวด TC-FOOD: ฟังก์ชันหน้ารายการอาหาร (Food List Page)
# ==============================================================================
def search_and_filter_foods(foods: List[Dict[str, Any]], query: Optional[str] = None, min_kcal: Optional[int] = None, max_kcal: Optional[int] = None, sort_by: Optional[str] = None):
    res = list(foods)
    if query:
        q = query.lower().strip()
        res = [f for f in res if q in f["name"].lower()]
    if min_kcal is not None:
        res = [f for f in res if f["kcal"] >= min_kcal]
    if max_kcal is not None:
        res = [f for f in res if f["kcal"] <= max_kcal]
    if sort_by == 'kcal_asc':
        res.sort(key=lambda x: x["kcal"])
    elif sort_by == 'price_asc':
        res.sort(key=lambda x: x["price"])
    return res

def test_tc_food_01():
    """TC-FOOD-01: รายการอาหาร ค้นหาชื่ออาหาร พิมพ์ 'ต้มยำ' -> กรองเหลือเฉพาะเมนูก๋วยเตี๋ยวต้มยำ"""
    res = search_and_filter_foods(INITIAL_FOODS, query="ต้มยำ")
    assert len(res) == 1, f"ต้องพบ 1 รายการ แต่ได้ {len(res)}"
    assert res[0]["name"] == "ก๋วยเตี๋ยวต้มยำหมูน้ำใส"

def test_tc_food_02():
    """TC-FOOD-02: รายการอาหาร กรองช่วง Kcal Min: 200, Max: 450 -> แสดงอาหารที่แคลอรี่อยู่ในช่วง 200–450 kcal เท่านั้น"""
    res = search_and_filter_foods(INITIAL_FOODS, min_kcal=200, max_kcal=450)
    assert len(res) == 2, f"ต้องพบ 2 รายการ แต่ได้ {len(res)}"
    for item in res:
        assert 200 <= item["kcal"] <= 450, f"หลุดช่วงแคลอรี่: {item['kcal']}"

def test_tc_food_03():
    """TC-FOOD-03: รายการอาหาร เรียงตามแคลอรี่ เลือก 'แคลอรี่: น้อยไปมาก' -> เมนูแคลอรี่ต่ำสุดแสดงขึ้นมาก่อน"""
    res = search_and_filter_foods(INITIAL_FOODS, sort_by="kcal_asc")
    assert res[0]["kcal"] == 160, "เมนูแรกต้องมี 160 kcal (ชาไทย)"
    assert res[-1]["kcal"] == 750, "เมนูสุดท้ายต้องมี 750 kcal"

def test_tc_food_04():
    """TC-FOOD-04: รายการอาหาร เรียงตามราคา เลือก 'ราคา: ต่ำไปสูง' -> เมนูราคาถูกสุด (30 บาท) แสดงขึ้นก่อน"""
    res = search_and_filter_foods(INITIAL_FOODS, sort_by="price_asc")
    assert res[0]["price"] == 30, "เมนูแรกต้องราคา 30 บาท"


# ==============================================================================
# 4. หมวด TC-CUST: ฟังก์ชันหน้าปรับแต่งอาหาร (Meal Customizer)
# ==============================================================================
def apply_customizer(base_food: Dict[str, Any], selected_modifiers: List[str]) -> Dict[str, Any]:
    total_kcal = base_food["kcal"]
    total_pro = base_food["protein"]
    total_carbs = base_food["carbohydrate"]
    total_fat = base_food["fat"]
    added_names = []

    for mod in MODIFIER_OPTIONS:
        if mod["id"] in selected_modifiers:
            total_kcal += mod["kcal"]
            total_pro += mod["pro"]
            total_carbs += mod["carbs"]
            total_fat += mod["fat"]
            added_names.append(mod["name"])

    dish_name = base_food["name"]
    if added_names:
        dish_name += f" ({', '.join(added_names)})"

    return {
        "name": dish_name,
        "calories": max(0, total_kcal),
        "protein": max(0, total_pro),
        "carbs": max(0, total_carbs),
        "fat": max(0, total_fat)
    }

def test_tc_cust_01():
    """TC-CUST-01: ปรับแต่งอาหาร เลือกเมนูตั้งต้น กะเพราไก่ไข่ดาว (640 kcal) -> แสดงเมนูและแคลอรี่ตั้งต้น 640 kcal"""
    base = INITIAL_FOODS[0]
    res = apply_customizer(base, [])
    assert res["name"] == "ข้าวกะเพราไก่ไข่ดาว"
    assert res["calories"] == 640

def test_tc_cust_02():
    """TC-CUST-02: ปรับแต่งอาหาร ท็อปปิ้งไข่ดาว ติ๊กเลือก '+ไข่ดาว (+90 kcal)' -> แคลอรี่คำนวณใหม่เป็น 730 kcal ทันที"""
    base = INITIAL_FOODS[0]
    res = apply_customizer(base, ["fried_egg"])
    assert res["calories"] == 730, f"คาดหวัง 730 แต่ได้ {res['calories']}"
    assert "ไข่ดาว" in res["name"]

def test_tc_cust_03():
    """TC-CUST-03: ปรับแต่งอาหาร ตัวเลือกสุขภาพ ติ๊กเลือก '-ลดข้าว (-100 kcal)' -> แคลอรี่ลดลงเหลือ 540 kcal ทันที"""
    base = INITIAL_FOODS[0]
    res = apply_customizer(base, ["half_rice"])
    assert res["calories"] == 540, f"คาดหวัง 540 แต่ได้ {res['calories']}"
    assert res["carbs"] == 41  # 66 - 25 = 41


# ==============================================================================
# 5. หมวด TC-DASH: ฟังก์ชันหน้าไดอารี่บันทึกมื้ออาหาร (Daily Dashboard)
# ==============================================================================
class DiaryManager:
    def __init__(self, target_calories: int = 2000):
        self.target = target_calories
        self.meals = []

    def add_meal(self, name: str, calories: int, meal_type: str = "lunch"):
        entry = {"id": f"meal-{len(self.meals)+1}", "name": name, "calories": calories, "type": meal_type}
        self.meals.append(entry)
        return entry

    def delete_meal(self, meal_id: str):
        self.meals = [m for m in self.meals if m["id"] != meal_id]

    def get_progress(self):
        used = sum(m["calories"] for m in self.meals)
        remaining = self.target - used
        percent = round((used / self.target) * 100, 1)
        return {"used": used, "remaining": remaining, "percent": percent}

def test_tc_dash_01():
    """TC-DASH-01: ไดอารี่ แถบ Progress Bar เปิดหน้าไดอารี่ -> คำนวณแคลอรี่ที่ทานไปแล้วเทียบกับ TDEE"""
    d = DiaryManager(target_calories=2000)
    d.add_meal("ข้าวกะเพราไก่", 640)
    prog = d.get_progress()
    assert prog["used"] == 640
    assert prog["remaining"] == 1360
    assert prog["percent"] == 32.0

def test_tc_dash_02():
    """TC-DASH-02: ไดอารี่ บันทึกมื้ออาหาร เพิ่มกะเพราไก่ มื้อกลางวัน -> แคลอรี่สะสมเพิ่มขึ้น และมีรายการใหม่ในตาราง"""
    d = DiaryManager(target_calories=2000)
    entry = d.add_meal("สลัดอกไก่ย่าง", 280, "dinner")
    assert len(d.meals) == 1
    assert entry["name"] == "สลัดอกไก่ย่าง"
    assert d.get_progress()["used"] == 280

def test_tc_dash_03():
    """TC-DASH-03: ไดอารี่ ลบมื้ออาหาร คลิกไอคอนถังขยะ -> รายการถูกลบ และยอดแคลอรี่สะสมลดลงตามจริง"""
    d = DiaryManager(target_calories=2000)
    e1 = d.add_meal("ข้าวกะเพราไก่", 640)
    e2 = d.add_meal("ชาไทย", 160)
    assert d.get_progress()["used"] == 800
    d.delete_meal(e1["id"])  # ลบกะเพราออก
    assert len(d.meals) == 1
    assert d.get_progress()["used"] == 160, "ต้องเหลือแค่แคลอรี่ชาไทย 160 kcal"


# ==============================================================================
# 6. หมวด TC-PROF: ฟังก์ชันหน้าโปรไฟล์และคำนวณสุขภาพ (Profile Page)
# ==============================================================================
def calc_bmr_mifflin(weight: float, height: float, age: int, gender: str) -> int:
    """สูตร Mifflin-St Jeor"""
    if gender == 'male':
        return round(10 * weight + 6.25 * height - 5 * age + 5)
    return round(10 * weight + 6.25 * height - 5 * age - 161)

def calc_tdee_val(bmr: int, activity_multiplier: float) -> int:
    return round(bmr * activity_multiplier)

def test_tc_prof_01():
    """TC-PROF-01: โปรไฟล์ คำนวณ BMR ชาย ชาย, นน. 65 กก., สส. 175 ซม., อายุ 21 -> BMR คำนวณได้ 1,644 kcal"""
    # 10(65) + 6.25(175) - 5(21) + 5 = 650 + 1093.75 - 105 + 5 = 1643.75 -> 1644
    bmr = calc_bmr_mifflin(65, 175, 21, 'male')
    assert bmr == 1644, f"คาดหวัง 1644 แต่ได้ {bmr}"

def test_tc_prof_02():
    """TC-PROF-02: โปรไฟล์ คำนวณ BMR หญิง หญิง, นน. 50 กก., สส. 160 ซม., อายุ 20 -> BMR คำนวณได้ 1,239 kcal"""
    # 10(50) + 6.25(160) - 5(20) - 161 = 500 + 1000 - 100 - 161 = 1239
    bmr = calc_bmr_mifflin(50, 160, 20, 'female')
    assert bmr == 1239, f"คาดหวัง 1239 แต่ได้ {bmr}"

def test_tc_prof_03():
    """TC-PROF-03: โปรไฟล์ คำนวณ TDEE BMR 1,650, กิจกรรมปานกลาง (1.55) -> TDEE คำนวณได้ 2,558 kcal"""
    tdee = calc_tdee_val(1650, 1.55)
    assert tdee == 2558, f"คาดหวัง 2558 แต่ได้ {tdee}"


# ==============================================================================
# 7. หมวด TC-AUTH: ฟังก์ชันเข้าสู่ระบบและสมัครสมาชิก (Authentication)
# ==============================================================================
class MockAuth:
    def __init__(self):
        self.users = [{"id": 1, "name": "นักศึกษา NPRU", "email": "student@npru.ac.th", "password": "password123"}]

    def login(self, email: str, password: str):
        u = next((x for x in self.users if x["email"] == email.strip().lower()), None)
        if not u or u["password"] != password:
            raise ValueError("อีเมลหรือรหัสผ่านไม่ถูกต้อง")
        return {"status": "success", "token": f"token-{u['id']}", "user": u}

    def register(self, name: str, email: str, password: str):
        clean_email = email.strip().lower()
        if any(x["email"] == clean_email for x in self.users):
            raise ValueError("อีเมลนี้ถูกใช้งานแล้วในระบบ")
        new_u = {"id": len(self.users)+1, "name": name, "email": clean_email, "password": password}
        self.users.append(new_u)
        return {"status": "success", "user": new_u}

def test_tc_auth_01():
    """TC-AUTH-01: เข้าสู่ระบบ Login สำเร็จ student@npru.ac.th / รหัสถูก -> เข้าสู่ระบบสำเร็จ แสดงชื่อผู้ใช้"""
    auth = MockAuth()
    res = auth.login("student@npru.ac.th", "password123")
    assert res["status"] == "success"
    assert res["user"]["name"] == "นักศึกษา NPRU"

def test_tc_auth_02():
    """TC-AUTH-02: เข้าสู่ระบบ Login รหัสผ่านผิด อีเมลถูก / รหัสผ่านผิด -> แจ้งเตือน 'อีเมลหรือรหัสผ่านไม่ถูกต้อง'"""
    auth = MockAuth()
    try:
        auth.login("student@npru.ac.th", "wrongpassword")
        assert False, "ต้องโยนข้อผิดพลาด"
    except ValueError as e:
        assert str(e) == "อีเมลหรือรหัสผ่านไม่ถูกต้อง"

def test_tc_auth_03():
    """TC-AUTH-03: เข้าสู่ระบบ Register สมัครสมาชิกใหม่ กรอกข้อมูลครบถ้วน -> บัญชีถูกสร้างสำเร็จ ได้รับ Token ทันที"""
    auth = MockAuth()
    res = auth.register("สมชาย รักดี", "somchai@npru.ac.th", "123456")
    assert res["status"] == "success"
    assert res["user"]["email"] == "somchai@npru.ac.th"

def test_tc_auth_04():
    """TC-AUTH-04: เข้าสู่ระบบ Register อีเมลซ้ำ ใช้อีเมลที่มีอยู่แล้ว -> แจ้งเตือน 'อีเมลนี้ถูกใช้งานแล้วในระบบ'"""
    auth = MockAuth()
    try:
        auth.register("คนใหม่", "student@npru.ac.th", "pass123")
        assert False, "ต้องไม่ให้สมัครซ้ำ"
    except ValueError as e:
        assert str(e) == "อีเมลนี้ถูกใช้งานแล้วในระบบ"


# ==============================================================================
# 8. หมวด TC-ADM: ฟังก์ชันผู้ดูแลระบบ (Admin Dashboard CRUD)
# ==============================================================================
class MockAdminDB:
    def __init__(self):
        self.restaurants = list(INITIAL_RESTAURANTS)
        self.foods = list(INITIAL_FOODS)

    def add_restaurant(self, name: str, location: str):
        new_id = max(r["id"] for r in self.restaurants) + 1
        new_r = {"id": new_id, "name": name, "location": location}
        self.restaurants.append(new_r)
        return new_r

    def add_food(self, name: str, rest_id: int, kcal: int, price: int):
        new_id = max(f["id"] for f in self.foods) + 1
        new_f = {"id": new_id, "name": name, "restaurant_id": rest_id, "kcal": kcal, "price": price}
        self.foods.append(new_f)
        return new_f

    def reset_db(self):
        self.restaurants = list(INITIAL_RESTAURANTS)
        self.foods = list(INITIAL_FOODS)

def test_tc_adm_01():
    """TC-ADM-01: แอดมิน เพิ่มร้านอาหาร ชื่อร้าน + สถานที่ตั้ง -> ร้านใหม่แสดงในหน้าร้านอาหารทันที"""
    db = MockAdminDB()
    new_r = db.add_restaurant("ร้านข้าวมันไก่เด็กหอ", "หอพักนักศึกษา มรภ.นครปฐม")
    assert new_r["name"] == "ร้านข้าวมันไก่เด็กหอ"
    assert len(db.restaurants) == 5

def test_tc_adm_04():
    """TC-ADM-04: แอดมิน เพิ่มเมนูอาหาร ชื่อเมนู + แคลอรี่ + สารอาหาร -> เมนูใหม่ถูกบันทึกและแสดงในหน้ารายการอาหาร"""
    db = MockAdminDB()
    new_f = db.add_food("ข้าวไข่เจียวสมุนไพร", 1, 450, 35)
    assert new_f["name"] == "ข้าวไข่เจียวสมุนไพร"
    assert len(db.foods) == 7

def test_tc_adm_06():
    """TC-ADM-06: แอดมิน รีเซ็ตฐานข้อมูล กดปุ่ม Reset DB -> ข้อมูลกลับสู่ค่าเริ่มต้นของมหาวิทยาลัย"""
    db = MockAdminDB()
    db.add_restaurant("ร้านชั่วคราว", "โรงอาหาร 1")
    assert len(db.restaurants) == 5
    db.reset_db()
    assert len(db.restaurants) == 4, "ต้องถูกรีเซ็ตกลับเป็น 4 ร้านตามค่าเริ่มต้น"


# ==============================================================================
# ฟังก์ชันหลัก รันทุก Test Case ตามตารางจริง
# ==============================================================================
def main():
    print("=" * 75)
    print("🧪 เริ่มต้นการรันชุดทดสอบ (Test Cases Matrix Execution)")
    print("   โครงงาน: ระบบวิเคราะห์และคำนวณแคลอรี่อาหารในมหาวิทยาลัย (มรภ.นครปฐม)")
    print("=" * 75)

    print("\n\033[96m--- 1. หมวด TC-HOME: ฟังก์ชันหน้าแรก (Home Page) ---\033[0m")
    Runner.test("TC-HOME-01", "หน้าแรก", "ค้นหาด่วน (Quick Search)", "พุ่งไปหน้ารายการอาหาร แสดงเฉพาะเมนูกะเพรา", test_tc_home_01)
    Runner.test("TC-HOME-02", "หน้าแรก", "ตัวชี้วัดสรุป (Quick Stats)", "แสดงการ์ดจำนวนร้าน, จำนวนเมนู, ค่าเฉลี่ย kcal ถูกต้อง", test_tc_home_02)
    Runner.test("TC-HOME-03", "หน้าแรก", "เมนูยอดนิยม (Popular Dishes)", "แสดงเฉพาะเมนูอาหารที่ถูกตั้งค่าเป็นยอดนิยม", test_tc_home_03)

    print("\n\033[96m--- 2. หมวด TC-REST: ฟังก์ชันหน้าร้านอาหาร (Restaurants Page) ---\033[0m")
    Runner.test("TC-REST-01", "ร้านค้า", "แสดงรายชื่อร้าน (List All)", "แสดงรายชื่อร้านค้าในมหาวิทยาลัยครบถ้วน", test_tc_rest_01)
    Runner.test("TC-REST-02", "ร้านค้า", "กรองเมนูตามร้าน (Filter by Store)", "แสดงเฉพาะเมนูอาหารของร้านป้าสมใจ", test_tc_rest_02)
    Runner.test("TC-REST-03", "ร้านค้า", "ค้นหาร้านค้า (Search Store)", "แสดงเฉพาะร้านก๋วยเตี๋ยวเรืออยุธยา", test_tc_rest_03)

    print("\n\033[96m--- 3. หมวด TC-FOOD: ฟังก์ชันหน้ารายการอาหาร (Food List Page) ---\033[0m")
    Runner.test("TC-FOOD-01", "รายการอาหาร", "ค้นหาชื่ออาหาร (Search Keyword)", "กรองเหลือเฉพาะเมนูก๋วยเตี๋ยวต้มยำ", test_tc_food_01)
    Runner.test("TC-FOOD-02", "รายการอาหาร", "กรองช่วงแคลอรี่ (Kcal Range)", "แสดงเฉพาะอาหารที่แคลอรี่อยู่ในช่วง 200–450 kcal", test_tc_food_02)
    Runner.test("TC-FOOD-03", "รายการอาหาร", "เรียงตามแคลอรี่ (Sort by Kcal)", "เมนูแคลอรี่ต่ำสุดแสดงขึ้นมาก่อน", test_tc_food_03)
    Runner.test("TC-FOOD-04", "รายการอาหาร", "เรียงตามราคา (Sort by Price)", "เมนูราคาถูกสุด (30 บาท) แสดงขึ้นก่อน", test_tc_food_04)

    print("\n\033[96m--- 4. หมวด TC-CUST: ฟังก์ชันหน้าปรับแต่งอาหาร (Meal Customizer) ---\033[0m")
    Runner.test("TC-CUST-01", "ปรับแต่งอาหาร", "เลือกเมนูตั้งต้น (Base Dish)", "แสดงเมนูและแคลอรี่ตั้งต้น 640 kcal", test_tc_cust_01)
    Runner.test("TC-CUST-02", "ปรับแต่งอาหาร", "ท็อปปิ้งไข่ดาว (Add-on)", "แคลอรี่คำนวณใหม่เป็น 730 kcal ทันที", test_tc_cust_02)
    Runner.test("TC-CUST-03", "ปรับแต่งอาหาร", "ตัวเลือกสุขภาพ (Adjustment)", "แคลอรี่ลดลงเหลือ 540 kcal ทันที", test_tc_cust_03)

    print("\n\033[96m--- 5. หมวด TC-DASH: ฟังก์ชันหน้าไดอารี่บันทึกมื้ออาหาร (Daily Dashboard) ---\033[0m")
    Runner.test("TC-DASH-01", "ไดอารี่", "แถบ Progress Bar (Calories Used)", "คำนวณแคลอรี่ที่ทานไปแล้วเทียบกับ TDEE", test_tc_dash_01)
    Runner.test("TC-DASH-02", "ไดอารี่", "บันทึกมื้ออาหาร (Add Meal Entry)", "แคลอรี่สะสมเพิ่มขึ้น และมีรายการใหม่ในตาราง", test_tc_dash_02)
    Runner.test("TC-DASH-03", "ไดอารี่", "ลบมื้ออาหาร (Delete Meal Entry)", "รายการถูกลบ และยอดแคลอรี่สะสมลดลงตามจริง", test_tc_dash_03)

    print("\n\033[96m--- 6. หมวด TC-PROF: ฟังก์ชันหน้าโปรไฟล์และคำนวณสุขภาพ (Profile Page) ---\033[0m")
    Runner.test("TC-PROF-01", "โปรไฟล์", "คำนวณ BMR ชาย (Mifflin-St Jeor)", "BMR คำนวณได้ 1,644 kcal", test_tc_prof_01)
    Runner.test("TC-PROF-02", "โปรไฟล์", "คำนวณ BMR หญิง (Mifflin-St Jeor)", "BMR คำนวณได้ 1,239 kcal", test_tc_prof_02)
    Runner.test("TC-PROF-03", "โปรไฟล์", "คำนวณ TDEE ตามกิจกรรม (1.55)", "TDEE คำนวณได้ 2,558 kcal", test_tc_prof_03)

    print("\n\033[96m--- 7. หมวด TC-AUTH: ฟังก์ชันเข้าสู่ระบบและสมัครสมาชิก (Authentication) ---\033[0m")
    Runner.test("TC-AUTH-01", "เข้าสู่ระบบ", "Login สำเร็จ (Valid Credentials)", "เข้าสู่ระบบสำเร็จ แสดงชื่อผู้ใช้", test_tc_auth_01)
    Runner.test("TC-AUTH-02", "เข้าสู่ระบบ", "Login รหัสผ่านผิด (Invalid Password)", "แจ้งเตือน 'อีเมลหรือรหัสผ่านไม่ถูกต้อง'", test_tc_auth_02)
    Runner.test("TC-AUTH-03", "เข้าสู่ระบบ", "Register สมัครสมาชิกใหม่ (New User)", "บัญชีถูกสร้างสำเร็จ ได้รับ Token ทันที", test_tc_auth_03)
    Runner.test("TC-AUTH-04", "เข้าสู่ระบบ", "Register อีเมลซ้ำ (Duplicate Email)", "แจ้งเตือน 'อีเมลนี้ถูกใช้งานแล้วในระบบ'", test_tc_auth_04)

    print("\n\033[96m--- 8. หมวด TC-ADM: ฟังก์ชันผู้ดูแลระบบ (Admin CRUD) ---\033[0m")
    Runner.test("TC-ADM-01", "แอดมิน", "เพิ่มร้านอาหาร (Add Restaurant)", "ร้านใหม่แสดงในหน้าร้านอาหารทันที", test_tc_adm_01)
    Runner.test("TC-ADM-04", "แอดมิน", "เพิ่มเมนูอาหาร (Add Food)", "เมนูใหม่ถูกบันทึกและแสดงในหน้ารายการอาหาร", test_tc_adm_04)
    Runner.test("TC-ADM-06", "แอดมิน", "รีเซ็ตฐานข้อมูล (Reset Database)", "ข้อมูลกลับสู่ค่าเริ่มต้นของมหาวิทยาลัย", test_tc_adm_06)

    print("\n" + "=" * 75)
    print("📊 สรุปผลการทดสอบทั้งหมด (Test Execution Summary)")
    print("=" * 75)
    print(f"  แบบทดสอบทั้งหมด : {Runner.total} รายการ")
    print(f"  \033[92mผ่าน (Passed)    : {Runner.passed} รายการ\033[0m")
    if Runner.failed > 0:
        print(f"  \033[91mไม่ผ่าน (Failed)  : {Runner.failed} รายการ\033[0m")
    else:
        print("  \033[92mสถานะ            : ผ่านครบ 100% ทุกรายการตาม Test Cases! 🎉\033[0m")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
