#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Test Case ID : TC-FOOD-01
หน้าจอ       : หน้ารายการอาหาร (Food List Page)
ฟังก์ชัน      : ค้นหาชื่ออาหารตามคีย์เวิร์ด (Search Food by Keyword)
ข้อมูลนำเข้า  : พิมพ์คำว่า "ต้มยำ" ในช่องค้นหา
ผลลัพธ์ที่คาดหวัง: กรองรายการอาหารเหลือเฉพาะเมนูก๋วยเตี๋ยวต้มยำ
================================================================================
"""

FOODS_DB = [
    {"id": 1, "name": "ข้าวกะเพราไก่ไข่ดาว", "category": "อาหารจานเดียว", "kcal": 640},
    {"id": 2, "name": "ก๋วยเตี๋ยวต้มยำหมูน้ำใส", "category": "ก๋วยเตี๋ยว", "kcal": 380},
    {"id": 3, "name": "ข้าวมันไก่ต้มพิเศษ", "category": "อาหารจานเดียว", "kcal": 590},
    {"id": 4, "name": "สลัดอกไก่ย่างคลีน", "category": "อาหารสุขภาพ", "kcal": 280},
    {"id": 5, "name": "ชาไทยเย็นหวานน้อย", "category": "เครื่องดื่ม", "kcal": 160},
]


def test_search_food_keyword():
    print("=" * 70)
    print("🧪 รันแบบทดสอบ: TC-FOOD-01 (หน้ารายการอาหาร - ค้นหาด้วยคำว่า 'ต้มยำ')")
    print("=" * 70)

    keyword = "ต้มยำ"
    print(f"👉 1. Input: ผู้ใช้กรอกคำค้นหา '{keyword}' ในหน้ารายการอาหาร")

    # 2. Logic การค้นหาอาหาร (Case-insensitive)
    matched_foods = [
        f for f in FOODS_DB
        if keyword.lower() in f["name"].lower()
    ]

    print(f"👉 2. ผลการค้นหา: พบ {len(matched_foods)} รายการ")
    for f in matched_foods:
        print(f"   🍲 {f['name']} ({f['category']}) - {f['kcal']} kcal")

    # 3. Assertions ตรวจสอบ
    assert len(matched_foods) == 1, f"ต้องพบ 1 รายการ แต่พบ {len(matched_foods)}"
    assert matched_foods[0]["name"] == "ก๋วยเตี๋ยวต้มยำหมูน้ำใส", "ชื่อเมนูต้องเป็นก๋วยเตี๋ยวต้มยำหมูน้ำใส"

    print("\n\033[92m✔ ผลการทดสอบ: ผ่าน (PASS) - กรองเมนูอาหารได้ตรงกับคำค้นหาอย่างแม่นยำ\033[0m\n")


if __name__ == "__main__":
    test_search_food_keyword()
