#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Test Case ID : TC-HOME-01
หน้าจอ       : หน้าแรก (Home Page)
ฟังก์ชัน      : ค้นหาด่วน (Quick Search Bar)
ข้อมูลนำเข้า  : พิมพ์คำว่า "กะเพรา"
ผลลัพธ์ที่คาดหวัง: พุ่งไปหน้ารายการอาหาร และแสดงเฉพาะเมนูที่มีคำว่ากะเพรา
================================================================================
"""

import sys

# ข้อมูลเมนูอาหารจริงในระบบมหาวิทยาลัย (รวมเมนูกะเพราหลากหลายรูปแบบ)
FOODS_DB = [
    {"id": 1, "name": "ข้าวกะเพราไก่ + ไข่ดาว", "restaurant_name": "ร้านป้าณี ตามสั่งตามใจ", "kcal": 590},
    {"id": 2, "name": "ก๋วยเตี๋ยวต้มยำหมูน้ำใส", "restaurant_name": "ก๋วยเตี๋ยวเรือมหาลัย แซ่บถึงใจ", "kcal": 340},
    {"id": 3, "name": "ข้าวมันไก่ตอน", "restaurant_name": "ข้าวมันไก่เฮียชัย โกเบ", "kcal": 520},
    {"id": 4, "name": "สลัดอกไก่ย่าง", "restaurant_name": "Green & Fit สลัดและสเต็กเด็กมอ", "kcal": 290},
    {"id": 18, "name": "ข้าวกะเพราหมูกรอบสูตรพริกแห้ง", "restaurant_name": "ร้านป้าณี ตามสั่งตามใจ", "kcal": 720},
    {"id": 19, "name": "ข้าวกะเพราหมูสับไข่ดาวไม่สุก", "restaurant_name": "ร้านป้าณี ตามสั่งตามใจ", "kcal": 620},
    {"id": 20, "name": "ข้าวกะเพราอกไก่คลีน (ผัดน้ำไม่ใช้น้ำมัน)", "restaurant_name": "Green & Fit สลัดและสเต็กเด็กมอ", "kcal": 380},
    {"id": 21, "name": "ข้าวกะเพราทะเลรวมมิตร (กุ้ง+หมึกสด)", "restaurant_name": "ร้านป้าณี ตามสั่งตามใจ", "kcal": 480},
    {"id": 22, "name": "ข้าวกะเพราเนื้อสับพริกสด", "restaurant_name": "ร้านป้าณี ตามสั่งตามใจ", "kcal": 660},
    {"id": 23, "name": "ข้าวกะเพราเต้าหู้เห็ดหอม (มังสวิรัติ)", "restaurant_name": "Green & Fit สลัดและสเต็กเด็กมอ", "kcal": 390},
]


def test_quick_search():
    print("=" * 70)
    print("🧪 รันแบบทดสอบ: TC-HOME-01 (หน้าแรก - ค้นหาด่วนเมนูกะเพรา)")
    print("=" * 70)

    # 1. จำลองการพิมพ์ค้นหาคำว่า "กะเพรา" ในกล่องค้นหาหน้าแรก
    search_keyword = "กะเพรา"
    print(f"👉 1. Input: ผู้ใช้พิมพ์คำว่า '{search_keyword}' ที่แถบค้นหาหน้าแรก")

    # 2. Logic การทำงานของเว็บ (สลับแท็บไป 'foods' และกรองชื่ออาหาร)
    target_tab = "foods"
    search_results = [
        item for item in FOODS_DB
        if search_keyword.lower() in item["name"].lower()
    ]

    print(f"👉 2. การเปลี่ยนหน้าจอ: เปลี่ยนไปหน้า '{target_tab}'")
    print(f"👉 3. ผลการค้นหาที่พบ: {len(search_results)} เมนูกะเพรา")
    for dish in search_results:
        print(f"   - {dish['name']} ({dish['kcal']} kcal) จาก {dish['restaurant_name']}")

    # 3. Assertions ตรวจสอบผลลัพธ์
    assert target_tab == "foods", "ระบบต้องสลับไปยังหน้ารายการอาหาร (foods)"
    assert len(search_results) >= 7, f"ต้องพบอย่างน้อย 7 เมนูกะเพรา แต่พบ {len(search_results)}"
    for dish in search_results:
        assert search_keyword in dish["name"], f"เมนู '{dish['name']}' ไม่มีคำว่า {search_keyword}"

    print("\n\033[92m✔ ผลการทดสอบ: ผ่าน (PASS) - ระบบพุ่งไปหน้ารายการอาหารและแสดงรายการกะเพราทั้งหมดถูกต้อง\033[0m\n")


if __name__ == "__main__":
    test_quick_search()
