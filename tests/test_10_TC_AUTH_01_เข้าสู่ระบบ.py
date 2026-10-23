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

from helpers import get_driver, quit_driver, APP_URL, By, WebDriverWait, EC


def test_selenium_tc_auth_01():
    print("=" * 70)
    print("🤖 Selenium Test: TC-AUTH-01 (เข้าสู่ระบบ - Login Modal ด้วย WebDriver)")
    print("=" * 70)

    driver = get_driver()

    try:
        driver.get(APP_URL)

        # Log out the demo session first so this test exercises the login form.
        user_menu = driver.find_elements(By.ID, "user-profile-menu-btn")
        if user_menu:
            user_menu[0].click()
            driver.find_element(By.XPATH, "//button[contains(., 'ออกจากระบบ')]").click()

        # 1. Open the login form.
        print("👉 1. ค้นหาและคลิกปุ่ม 'เข้าสู่ระบบ' บน Navbar")
        login_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "nav-login-btn")))
        login_btn.click()

        # 2. Enter credentials and submit the actual login form.
        input_email = "student@npru.ac.th"
        input_pass = "password123"
        email_field = driver.find_element(By.ID, "input-email")
        password_field = driver.find_element(By.ID, "input-password")
        email_field.clear()
        email_field.send_keys(input_email)
        password_field.clear()
        password_field.send_keys(input_pass)
        driver.find_element(By.ID, "btn-auth-submit").click()

        print(f"👉 2. ส่งฟอร์มเข้าสู่ระบบ: Email='{input_email}', Password='***'")
        login_success = WebDriverWait(driver, 10).until(
            lambda current_driver: current_driver.find_elements(By.ID, "user-profile-menu-btn")
        )
        logged_in_name = login_success[0].text
        print(f"👉 3. ผลลัพธ์บน Navbar: {logged_in_name}")
        assert logged_in_name.strip(), "Navbar ต้องแสดงชื่อผู้ใช้หลังเข้าสู่ระบบสำเร็จ"

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - เข้าสู่ระบบและแสดงสถานะผู้ใช้สำเร็จ\033[0m\n")

    finally:
        quit_driver(driver)


if __name__ == "__main__":
    test_selenium_tc_auth_01()
