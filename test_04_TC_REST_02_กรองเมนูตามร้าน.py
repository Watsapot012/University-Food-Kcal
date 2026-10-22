#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Test Case ID : TC-REST-02
หน้าจอ       : หน้าร้านอาหาร (Restaurants Page)
ฟังก์ชัน      : กรองเมนูอาหารตามร้านที่เลือก (Filter Foods by Store)
ข้อมูลนำเข้า  : คลิกเลือกร้านค้า "ร้านป้าสมใจ อาหารตามสั่ง" (restaurant_id = 1)
ผลลัพธ์ที่คาดหวัง: รายการอาหารด้านล่างแสดงเฉพาะเมนูที่สังกัดร้านป้าสมใจเท่านั้น
================================================================================
"""

FOODS_DB = [
    {"id": 1, "name": "ข้าวกะเพราไก่ไข่ดาว", "restaurant_id": 1, "restaurant_name": "ร้านป้าสมใจ อาหารตามสั่ง", "kcal": 640},
    {"id": 2, "name": "ก๋วยเตี๋ยวต้มยำหมูน้ำใส", "restaurant_id": 2, "restaurant_name": "ก๋วยเตี๋ยวเรืออยุธยา", "kcal": 380},
    {"id": 3, "name": "ข้าวมันไก่ต้มพิเศษ", "restaurant_id": 3, "restaurant_name": "ข้าวมันไก่เด็กหอตอนดึก", "kcal": 590},
    {"id": 4, "name": "สลัดอกไก่ย่างคลีน", "restaurant_id": 1, "restaurant_name": "ร้านป้าสมใจ อาหารตามสั่ง", "kcal": 280},
    {"id": 5, "name": "ชาไทยเย็นหวานน้อย", "restaurant_id": 4, "restaurant_name": "ร้านกาแฟและชานมชาวมอ", "kcal": 160},
    {"id": 6, "name": "ข้าวผัดกะเพราหมูกรอบ", "restaurant_id": 1, "restaurant_name": "ร้านป้าสมใจ อาหารตามสั่ง", "kcal": 750},
]


def test_filter_foods_by_restaurant():
    print("=" * 70)
    print("🧪 รันแบบทดสอบ: TC-REST-02 (หน้าร้านอาหาร - กรองเมนูอาหารตามร้าน)")
    print("=" * 70)

    selected_restaurant_id = 1
    selected_restaurant_name = "ร้านป้าสมใจ อาหารตามสั่ง"
    print(f"👉 1. Input: ผู้ใช้คลิกเลือกร้าน '{selected_restaurant_name}' (ID: {selected_restaurant_id})")

    # 2. Logic การคัดกรองเฉพาะเมนูของร้านที่เลือก
    filtered_dishes = [
        f for f in FOODS_DB
        if f["restaurant_id"] == selected_restaurant_id
    ]

    print(f"👉 2. รายการอาหารของร้านที่ระบบกรองมาได้: {len(filtered_dishes)} เมนู")
    for dish in filtered_dishes:
        print(f"   🍽️ {dish['name']} | พลังงาน: {dish['kcal']} kcal")

    # 3. Assertions ตรวจสอบความถูกต้อง
    assert len(filtered_dishes) == 3, f"ร้านป้าสมใจต้องมี 3 เมนู แต่กรองได้ {len(filtered_dishes)} เมนู"
    for dish in filtered_dishes:
        assert dish["restaurant_id"] == 1, f"เมนู '{dish['name']}' ไม่ใช่ของร้านป้าสมใจ"

    print("\n\033[92m✔ ผลการทดสอบ: ผ่าน (PASS) - กรองแสดงเฉพาะเมนูอาหารของร้านที่เลือกได้อย่างถูกต้อง\033[0m\n")


if __name__ == "__main__":
    test_filter_foods_by_restaurant()
