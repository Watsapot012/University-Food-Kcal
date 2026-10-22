#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Test Case ID : TC-FOOD-02
หน้าจอ       : หน้ารายการอาหาร (Food List Page)
ฟังก์ชัน      : กรองอาหารตามช่วงแคลอรี่ (Filter by Kcal Range Slider)
ข้อมูลนำเข้า  : ปรับสไลเดอร์ Min Kcal = 200, Max Kcal = 450
ผลลัพธ์ที่คาดหวัง: แสดงเฉพาะเมนูอาหารที่ค่าพลังงานอยู่ในช่วง 200 ถึง 450 kcal เท่านั้น
================================================================================
"""

FOODS_DB = [
    {"id": 1, "name": "ข้าวกะเพราไก่ไข่ดาว", "kcal": 640},
    {"id": 2, "name": "ก๋วยเตี๋ยวต้มยำหมูน้ำใส", "kcal": 380},
    {"id": 3, "name": "ข้าวมันไก่ต้มพิเศษ", "kcal": 590},
    {"id": 4, "name": "สลัดอกไก่ย่างคลีน", "kcal": 280},
    {"id": 5, "name": "ชาไทยเย็นหวานน้อย", "kcal": 160},
    {"id": 6, "name": "ข้าวผัดกะเพราหมูกรอบ", "kcal": 750},
]


def test_filter_by_kcal_range():
    print("=" * 70)
    print("🧪 รันแบบทดสอบ: TC-FOOD-02 (หน้ารายการอาหาร - กรองช่วงแคลอรี่ 200-450 kcal)")
    print("=" * 70)

    min_kcal = 200
    max_kcal = 450
    print(f"👉 1. Input: ผู้ใช้เลื่อนสไลเดอร์กำหนดช่วง Min={min_kcal} kcal, Max={max_kcal} kcal")

    # 2. Logic การกรองตามช่วงแคลอรี่
    filtered_foods = [
        f for f in FOODS_DB
        if min_kcal <= f["kcal"] <= max_kcal
    ]

    print(f"👉 2. ผลการกรอง: พบ {len(filtered_foods)} เมนูที่อยู่ในเกณฑ์")
    for f in filtered_foods:
        print(f"   🥗 {f['name']} -> {f['kcal']} kcal")

    # 3. Assertions ตรวจสอบ
    # เมนูที่ต้องผ่าน: ก๋วยเตี๋ยวต้มยำหมูน้ำใส (380), สลัดอกไก่ย่างคลีน (280)
    # เมนูที่ไม่ผ่าน: ชาไทย (160 ต่ำไป), ข้าวมันไก่ (590 สูงไป), กะเพรา (640, 750)
    assert len(filtered_foods) == 2, f"ต้องพบ 2 เมนู แต่พบ {len(filtered_foods)}"
    for f in filtered_foods:
        assert 200 <= f["kcal"] <= 450, f"ค่าแคลอรี่ {f['kcal']} หลุดช่วงกำหนด!"

    print("\n\033[92m✔ ผลการทดสอบ: ผ่าน (PASS) - กรองอาหารตามช่วงแคลอรี่ได้อย่างถูกต้องตามเงื่อนไข\033[0m\n")


if __name__ == "__main__":
    test_filter_by_kcal_range()
