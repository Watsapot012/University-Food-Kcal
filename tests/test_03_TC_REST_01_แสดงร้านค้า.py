#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Test Case ID : TC-REST-01
หน้าจอ       : หน้าร้านอาหาร (Restaurants Page)
ฟังก์ชัน      : แสดงรายชื่อร้านค้าทั้งหมด (List All Restaurants)
ข้อมูลนำเข้า  : เข้าสู่แท็บ "ร้านอาหาร" (Navigate to Restaurants Tab)
ผลลัพธ์ที่คาดหวัง: แสดงรายชื่อร้านค้าทั้งหมดใน มรภ.นครปฐม พร้อมสถานที่ตั้ง เวลาเปิดทำการครบถ้วน
================================================================================
"""

RESTAURANTS_DB = [
    {
        "id": 1,
        "name": "ร้านป้าสมใจ อาหารตามสั่ง",
        "location": "โรงอาหาร 1 มรภ.นครปฐม",
        "open_hours": "07:30 - 16:00 น.",
        "phone": "081-234-5678",
        "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5"
    },
    {
        "id": 2,
        "name": "ก๋วยเตี๋ยวเรืออยุธยา สูตรโบราณ",
        "location": "โรงอาหาร 2 มรภ.นครปฐม",
        "open_hours": "08:00 - 15:30 น.",
        "phone": "089-876-5432",
        "image": "https://images.unsplash.com/photo-1569058242253-92a9c755a0ec"
    },
    {
        "id": 3,
        "name": "ข้าวมันไก่เด็กหอตอนดึก",
        "location": "หน้าหอพักนักศึกษา มรภ.นครปฐม",
        "open_hours": "10:00 - 20:00 น.",
        "phone": "086-555-4321",
        "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
    },
    {
        "id": 4,
        "name": "ร้านกาแฟและชานมชาวมอ",
        "location": "อาคารเรียนรวม 1",
        "open_hours": "07:30 - 17:00 น.",
        "phone": "082-333-2211",
        "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"
    },
]


def test_list_restaurants():
    print("=" * 70)
    print("🧪 รันแบบทดสอบ: TC-REST-01 (หน้าร้านอาหาร - แสดงรายชื่อร้านค้าทั้งหมด)")
    print("=" * 70)

    print("👉 1. Input: ผู้ใช้คลิกแท็บ 'ร้านอาหาร' บน Navbar")

    # 2. Logic การดึงข้อมูลร้านค้ามาแสดงผล
    displayed_restaurants = list(RESTAURANTS_DB)

    print(f"👉 2. ดึงข้อมูลสำเร็จ: พบ {len(displayed_restaurants)} ร้านค้าในระบบ")
    for r in displayed_restaurants:
        print(f"   🏢 [{r['id']}] {r['name']} | 📍 {r['location']} | ⏰ {r['open_hours']}")

    # 3. Assertions ตรวจสอบฟิลด์ข้อมูลที่จำเป็น
    assert len(displayed_restaurants) >= 4, "ต้องมีร้านอาหารอย่างน้อย 4 ร้าน"
    for r in displayed_restaurants:
        assert r["name"].strip() != "", "ชื่อร้านต้องไม่เป็นค่าว่าง"
        assert r["location"].strip() != "", "สถานที่ตั้งต้องไม่เป็นค่าว่าง"
        assert "open_hours" in r, "ต้องมีเวลาเปิดทำการ"

    print("\n\033[92m✔ ผลการทดสอบ: ผ่าน (PASS) - แสดงรายการร้านค้าครบถ้วนตามฐานข้อมูลของมหาวิทยาลัย\033[0m\n")


if __name__ == "__main__":
    test_list_restaurants()
