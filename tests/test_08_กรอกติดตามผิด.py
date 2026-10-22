#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 08: ทดสอบกรณีค้นหา/ติดตามข้อมูลผิดพลาด หรือระบุข้อมูลไม่มีในระบบ
ฟังก์ชัน: GET /api/foods/:id และ GET /api/restaurants/:id (Error & Boundary Cases)
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import ApiClient

def test_track_invalid_not_found():
    """ทดสอบการติดตามหรือค้นหาข้อมูลด้วย ID หรือเงื่อนไขที่ไม่มีอยู่จริง"""
    client = ApiClient()

    # กรณี 1: ค้นหาอาหารด้วยรหัส ID ที่ไม่มีในระบบ (999999)
    status_food, res_food = client.get("/foods/999999")
    print(f"\n[Test 08.1] GET /api/foods/999999 (ค้นหาอาหารไม่มีอยู่จริง):")
    print(f"  Response Status: {status_food}")
    print(f"  Response Body: {res_food}")
    assert status_food == 404, f"คาดหวัง Status 404 Not Found แต่ได้ {status_food}"
    assert "error" in res_food, "ต้องมีข้อความ error ไม่พบรายการอาหาร"

    # กรณี 2: ค้นหาร้านอาหารด้วย ID ที่ไม่มีในระบบ (888888)
    status_rest, res_rest = client.get("/restaurants/888888")
    print(f"\n[Test 08.2] GET /api/restaurants/888888 (ค้นหาร้านไม่มีอยู่จริง):")
    print(f"  Response Status: {status_rest}")
    assert status_rest == 404, f"คาดหวัง Status 404 Not Found แต่ได้ {status_rest}"

    # กรณี 3: ค้นหาด้วยคีย์เวิร์ดที่ไม่มีในระบบ
    status_search, res_search = client.get("/foods?search=เมนูที่ไม่มีอยู่จริง12345xyz")
    assert status_search == 200, "ค้นหาต้องตอบกลับ 200 เป็น Array ว่าง"
    assert len(res_search) == 0, "ผลการค้นหาคำที่ไม่มีต้องเป็นลิสต์ว่าง"

    print("  \033[92m✔ ผ่านการทดสอบ: ระบบจัดการข้อผิดพลาด Not Found (404) และการค้นหาได้อย่างถูกต้อง\033[0m")
    return True

if __name__ == "__main__":
    test_track_invalid_not_found()
