#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 05: ทดสอบกรณีผู้ใช้กรอกแบบฟอร์มผิดพลาด / ข้อมูลไม่ครบ (Form Validation Error)
ฟังก์ชัน: POST /api/logs และ POST /api/foods (Negative Test Case)
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import ApiClient

def test_form_validation_errors():
    """ทดสอบส่งแบบฟอร์มที่เว้นว่างฟิลด์สำคัญ หรือข้อมูลไม่ถูกต้อง"""
    client = ApiClient()

    # กรณี 1: บันทึกอาหารโดยไม่ระบุชื่ออาหาร
    invalid_log = {
        "userId": 1,
        "name": "",
        "calories": 500
    }
    status, response = client.post("/logs", data=invalid_log)
    print(f"\n[Test 05.1] ส่งฟอร์มบันทึกมื้ออาหารโดยไม่ระบุชื่อ:")
    print(f"  Response Status: {status}")
    print(f"  Response Body: {response}")
    assert status == 400, f"คาดหวัง Status 400 แต่ได้ {status}"
    assert "error" in response, "ต้องส่งข้อความ error กลับมา"

    # กรณี 2: เพิ่มเมนูอาหารโดยไม่เลือกร้านค้า
    invalid_food = {
        "name": "ข้าวผัดกระเทียม",
        "price": 50
        # ขาด restaurant_id
    }
    status_food, res_food = client.post("/foods", data=invalid_food)
    print(f"\n[Test 05.2] ส่งฟอร์มเพิ่มเมนูอาหารโดยไม่ระบุร้านค้า:")
    print(f"  Response Status: {status_food}")
    print(f"  Response Body: {res_food}")
    assert status_food == 400, f"คาดหวัง Status 400 แต่ได้ {status_food}"

    print("  \033[92m✔ ผ่านการทดสอบ: ระบบตรวจสอบ Validation ฟอร์มและปฏิเสธข้อมูลไม่สมบูรณ์ถูกต้อง\033[0m")
    return True

if __name__ == "__main__":
    test_form_validation_errors()
