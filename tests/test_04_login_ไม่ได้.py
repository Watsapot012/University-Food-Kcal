#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 04: ทดสอบกรณีเข้าสู่ระบบไม่สำเร็จ (Login Failed / Invalid Credentials)
ฟังก์ชัน: POST /api/auth/login (Negative Test Case)
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import ApiClient

def test_login_failed_wrong_password():
    """ทดสอบกรณีป้อนรหัสผ่านไม่ถูกต้อง หรืออีเมลไม่มีในระบบ"""
    client = ApiClient()

    # กรณีที่ 1: รหัสผ่านผิด
    payload_wrong_pw = {
        "email": "student@npru.ac.th",
        "password": "wrong_password_999"
    }
    status, response = client.post("/auth/login", data=payload_wrong_pw)

    print(f"\n[Test 04.1] Login ด้วยรหัสผ่านผิด: POST /api/auth/login")
    print(f"  Response Status: {status}")
    print(f"  Response Body: {response}")

    assert status == 401, f"คาดหวัง Status 401 Unauthorized แต่ได้ {status}"
    assert "error" in response, "ต้องมีข้อความ error ตอบกลับ"

    # กรณีที่ 2: ไม่ระบุรหัสผ่านหรืออีเมล
    status_empty, res_empty = client.post("/auth/login", data={"email": ""})
    print(f"\n[Test 04.2] Login โดยไม่กรอกข้อมูล:")
    print(f"  Response Status: {status_empty}")
    assert status_empty == 400, f"คาดหวัง Status 400 Bad Request แต่ได้ {status_empty}"

    print("  \033[92m✔ ผ่านการทดสอบ: ระบบป้องกันการ Login ผิดพลาดได้อย่างถูกต้อง\033[0m")
    return True

if __name__ == "__main__":
    test_login_failed_wrong_password()
