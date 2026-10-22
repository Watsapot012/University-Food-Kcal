#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 01: ทดสอบการเข้าสู่ระบบสำเร็จ (Login Success)
ฟังก์ชัน: POST /api/auth/login
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import ApiClient, save_state

def test_login_success():
    """ทดสอบการล็อกอินด้วยอีเมลและรหัสผ่านที่ถูกต้อง"""
    client = ApiClient()
    payload = {
        "email": "student@npru.ac.th",
        "password": "password123"
    }

    status, response = client.post("/auth/login", data=payload)

    print(f"\n[Test 01] POST /api/auth/login")
    print(f"  Payload: {payload}")
    print(f"  Response Status: {status}")
    print(f"  Response Body: {response}")

    assert status == 200, f"คาดหวัง Status 200 แต่ได้ {status}"
    assert "token" in response, "ต้องได้รับ token ตอบกลับ"
    assert "user" in response, "ต้องมีข้อมูล user ตอบกลับ"
    assert response["user"]["email"] == "student@npru.ac.th", "อีเมลผู้ใช้ต้องตรงกัน"

    # บันทึก token ลง State เพื่อใช้ในเคสถัดไป
    save_state({
        "token": response["token"],
        "userId": response["user"]["id"],
        "userEmail": response["user"]["email"]
    })
    print("  \033[92m✔ ผ่านการทดสอบ: เข้าสู่ระบบสำเร็จและได้รับ Token เรียบร้อย\033[0m")
    return True

if __name__ == "__main__":
    test_login_success()
