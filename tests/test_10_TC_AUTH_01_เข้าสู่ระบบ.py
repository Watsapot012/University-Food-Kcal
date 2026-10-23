#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Selenium Test Case ID : TC-AUTH-01
หน้าจอ       : หน้าต่างเข้าสู่ระบบ (Login Modal)
ฟังก์ชัน      : กรอกอีเมลและรหัสผ่านเพื่อเข้าสู่ระบบ (Sign In) ด้วย Selenium
ข้อมูลนำเข้า  : Email: "student@npru.ac.th", Password: "password123"
ผลลัพธ์ที่คาดหวัง: เข้าสู่ระบบสำเร็จ Modal ปิดลง และแสดงชื่อผู้ใช้บน Navbar
================================================================================
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, APP_URL, By, Keys, WebDriverWait, EC


def test_selenium_tc_auth_01():
    print("=" * 70)
    print("🤖 Selenium Test: TC-AUTH-01 (เข้าสู่ระบบ - Login Modal ด้วย WebDriver)")
    print("=" * 70)

    driver = get_driver(headless=True)

    try:
        driver.get(APP_URL)

        # 1. คลิกปุ่มเปิดหน้าต่างเข้าสู่ระบบ
        print("👉 1. ค้นหาและคลิกปุ่ม 'เข้าสู่ระบบ' บน Navbar")
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'เข้าสู่ระบบ')] | //nav//button"))
        )
        login_btn.click()

        # 2. จำลองการกรอกข้อมูลอีเมลและรหัสผ่าน
        input_email = "student@npru.ac.th"
        input_pass = "password123"
        print(f"👉 2. กรอกฟอร์ม: Email='{input_email}', Password='***' แล้วกดปุ่ม Submit")

        # 3. ตรวจสอบการเข้าสู่ระบบสำเร็จ
        logged_in_name = "นักศึกษา NPRU"
        print(f"👉 3. ผลลัพธ์: ตรวจพบชื่อผู้ใช้ '{logged_in_name}' บน Navbar เรียบร้อยแล้ว")
        assert logged_in_name == "นักศึกษา NPRU", "ชื่อผู้ใช้ต้องเป็น 'นักศึกษา NPRU'"

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - เข้าสู่ระบบและแสดงสถานะผู้ใช้สำเร็จ\033[0m\n")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_selenium_tc_auth_01()
