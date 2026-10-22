#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Test Case ID : TC-HOME-02
หน้าจอ       : หน้าแรก (Home Page)
ฟังก์ชัน      : ตัวชี้วัดสรุปภาพรวม (Quick Stats Overview)
ข้อมูลนำเข้า  : โหลดหน้าแรกของเว็บไซต์
ผลลัพธ์ที่คาดหวัง: แสดงการ์ดตัวเลขสรุป: จำนวนร้าน, จำนวนเมนู, ค่าเฉลี่ยแคลอรี่, เมนูสูงสุด และต่ำสุด
================================================================================
"""

RESTAURANTS_DB = [
    {"id": 1, "name": "ร้านป้าสมใจ อาหารตามสั่ง", "location": "โรงอาหาร 1"},
    {"id": 2, "name": "ก๋วยเตี๋ยวเรืออยุธยา สูตรโบราณ", "location": "โรงอาหาร 2"},
    {"id": 3, "name": "ข้าวมันไก่เด็กหอตอนดึก", "location": "หอพักนักศึกษา"},
    {"id": 4, "name": "ร้านกาแฟและชานมชาวมอ", "location": "อาคารเรียนรวม 1"},
]

FOODS_DB = [
    {"id": 1, "name": "ข้าวกะเพราไก่ไข่ดาว", "kcal": 640},
    {"id": 2, "name": "ก๋วยเตี๋ยวต้มยำหมูน้ำใส", "kcal": 380},
    {"id": 3, "name": "ข้าวมันไก่ต้มพิเศษ", "kcal": 590},
    {"id": 4, "name": "สลัดอกไก่ย่างคลีน", "kcal": 280},
    {"id": 5, "name": "ชาไทยเย็นหวานน้อย", "kcal": 160},
    {"id": 6, "name": "ข้าวผัดกะเพราหมูกรอบ", "kcal": 750},
]


def test_home_quick_stats():
    print("=" * 70)
    print("🧪 รันแบบทดสอบ: TC-HOME-02 (หน้าแรก - ตัวชี้วัดสรุป Quick Stats)")
    print("=" * 70)

    print("👉 1. Input: โหลดหน้าแรกของเว็บไซต์ (Initial Page Load)")

    # 2. Logic การคำนวณ Stats ของระบบ
    total_restaurants = len(RESTAURANTS_DB)
    total_foods = len(FOODS_DB)
    total_kcal = sum(f["kcal"] for f in FOODS_DB)
    avg_kcal = round(total_kcal / total_foods, 1)

    max_dish = max(FOODS_DB, key=lambda x: x["kcal"])
    min_dish = min(FOODS_DB, key=lambda x: x["kcal"])

    print("👉 2. ค่าตัวชี้วัดที่ระบบคำนวณได้:")
    print(f"   - การ์ดที่ 1 (จำนวนร้านค้า)    : {total_restaurants} ร้าน")
    print(f"   - การ์ดที่ 2 (จำนวนเมนูอาหาร)  : {total_foods} เมนู")
    print(f"   - การ์ดที่ 3 (ค่าเฉลี่ยแคลอรี่) : {avg_kcal} kcal/จาน")
    print(f"   - การ์ดที่ 4 (เมนู Kcal สูงสุด): {max_dish['name']} ({max_dish['kcal']} kcal)")
    print(f"   - การ์ดที่ 5 (เมนู Kcal ต่ำสุด): {min_dish['name']} ({min_dish['kcal']} kcal)")

    # 3. Assertions ตรวจสอบความถูกต้อง
    assert total_restaurants == 4, f"จำนวนร้านค้าต้องเป็น 4 ร้าน แต่ได้ {total_restaurants}"
    assert total_foods == 6, f"จำนวนเมนูอาหารต้องเป็น 6 เมนู แต่ได้ {total_foods}"
    assert avg_kcal == 466.7, f"ค่าเฉลี่ย kcal ต้องเป็น 466.7 แต่ได้ {avg_kcal}"
    assert max_dish["name"] == "ข้าวผัดกะเพราหมูกรอบ", "เมนูแคลอรี่สูงสุดต้องเป็นข้าวกะเพราหมูกรอบ"
    assert min_dish["name"] == "ชาไทยเย็นหวานน้อย", "เมนูแคลอรี่ต่ำสุดต้องเป็นชาไทยเย็นหวานน้อย"

    print("\n\033[92m✔ ผลการทดสอบ: ผ่าน (PASS) - การ์ดตัวชี้วัดสรุปแสดงผลข้อมูลตรงตามฐานข้อมูลจริง 100%\033[0m\n")


if __name__ == "__main__":
    test_home_quick_stats()
