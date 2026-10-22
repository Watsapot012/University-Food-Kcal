#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 02: ทดสอบการกรอกแบบฟอร์มและกดส่งข้อมูล (Form Submission: บันทึกมื้ออาหารประจำวัน)
ฟังก์ชัน: POST /api/logs
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import ApiClient, load_state, save_state

def test_submit_meal_log():
    """ทดสอบกรอกข้อมูลแบบฟอร์มบันทึกอาหารแล้วกดส่งเข้าสู่ระบบ"""
    client = ApiClient()
    state = load_state()
    user_id = state.get("userId", 1)

    payload = {
        "userId": user_id,
        "name": "ข้าวกะเพราหมูกรอบ + ไข่ดาว (พิเศษ)",
        "calories": 680,
        "type": "lunch",
        "protein": 32,
        "carbs": 60,
        "fat": 34
    }

    status, response = client.post("/logs", data=payload)

    print(f"\n[Test 02] POST /api/logs (กรอกแบบฟอร์มบันทึกอาหาร)")
    print(f"  Payload: {payload}")
    print(f"  Response Status: {status}")
    print(f"  Response Body: {response}")

    assert status == 201, f"คาดหวัง Status 201 Created แต่ได้ {status}"
    assert "id" in response, "ต้องได้ id ของ Log รายการอาหารที่ถูกบันทึก"
    assert response["calories"] == 680, "จำนวนแคลอรี่ต้องตรงกับฟอร์มที่กรอก"
    assert response["name"] == payload["name"], "ชื่ออาหารต้องตรงกับฟอร์มที่กรอก"

    # บันทึก ID รายการที่เพิ่งสร้างเพื่อนำไปทดสอบเคสถัดไป
    save_state({"lastCreatedLogId": response["id"]})
    print("  \033[92m✔ ผ่านการทดสอบ: กรอกแบบฟอร์มและบันทึกข้อมูลเข้าสู่ระบบสำเร็จ\033[0m")
    return True

if __name__ == "__main__":
    test_submit_meal_log()
