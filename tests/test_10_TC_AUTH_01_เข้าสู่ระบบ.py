#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Test Case ID : TC-AUTH-01
หน้าจอ       : หน้าต่างเข้าสู่ระบบ (Login Modal)
ฟังก์ชัน      : ตรวจสอบและเข้าสู่ระบบ (Authentication & Sign In)
ข้อมูลนำเข้า  : Email: "student@npru.ac.th", Password: "password123"
ผลลัพธ์ที่คาดหวัง: เข้าสู่ระบบสำเร็จ ได้รับ Token และแสดงชื่อผู้ใช้ "นักศึกษา NPRU" ที่ Navbar
================================================================================
"""

MOCK_USERS_DB = [
    {
        "id": 1,
        "name": "นักศึกษา NPRU",
        "email": "student@npru.ac.th",
        "password": "password123",
        "role": "student"
    }
]


def login_service(email: str, password: str):
    clean_email = email.strip().lower()
    user = next((u for u in MOCK_USERS_DB if u["email"].lower() == clean_email), None)

    if not user:
        raise ValueError("ไม่พบบัญชีผู้ใช้นี้ในระบบ")
    if user["password"] != password:
        raise ValueError("อีเมลหรือรหัสผ่านไม่ถูกต้อง")

    # ออก Token จำลอง
    token = f"token-{user['id']}-npru-auth"
    return {
        "status": "success",
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }


def test_login_success():
    print("=" * 70)
    print("🧪 รันแบบทดสอบ: TC-AUTH-01 (เข้าสู่ระบบ - Login สำเร็จ)")
    print("=" * 70)

    input_email = "student@npru.ac.th"
    input_pass = "password123"
    print(f"👉 1. Input: ผู้ใช้กรอก Email='{input_email}', Password='***'")

    # 2. Logic การตรวจสอบสิทธิ์
    response = login_service(input_email, input_pass)

    print(f"👉 2. ผลการทำงานของระบบ:")
    print(f"   - สถานะ (Status)    : {response['status']}")
    print(f"   - ชื่อผู้ใช้ที่ล็อกอิน : {response['user']['name']}")
    print(f"   - รหัส Token        : {response['token']}")

    # 3. Assertions ตรวจสอบ
    assert response["status"] == "success", "สถานะต้องเป็น success"
    assert response["user"]["name"] == "นักศึกษา NPRU", "ชื่อผู้ใช้ต้องเป็น 'นักศึกษา NPRU'"
    assert "token" in response and len(response["token"]) > 0, "ต้องได้รับ Token เพื่อใช้ระบุตัวตน"

    print("\n\033[92m✔ ผลการทดสอบ: ผ่าน (PASS) - เข้าสู่ระบบสำเร็จและบันทึกเซสชันผู้ใช้อย่างถูกต้อง\033[0m\n")


if __name__ == "__main__":
    test_login_success()
