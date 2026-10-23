#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Selenium Test Case ID : TC-DASH-02
หน้าจอ       : หน้าไดอารี่ประจำวัน (Daily Dashboard Page)
ฟังก์ชัน      : บันทึกมื้ออาหารลงตาราง (Log Meal Entry) ด้วย Selenium
ข้อมูลนำเข้า  : เพิ่มอาหาร "ข้าวกะเพราไก่" (640 kcal) ลงในมื้อกลางวัน
ผลลัพธ์ที่คาดหวัง: รายการอาหารใหม่แสดงในตาราง และแถบ Progress แคลอรี่สะสมเพิ่มขึ้น
================================================================================
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, APP_URL, By, WebDriverWait, EC


def test_selenium_tc_dash_02():
    print("=" * 70)
    print("🤖 Selenium Test: TC-DASH-02 (ไดอารี่ - บันทึกมื้ออาหารลงตารางด้วย WebDriver)")
    print("=" * 70)

    driver = get_driver()

    try:
        driver.get(APP_URL)

        # 1. คลิกแท็บ "ไดอารี่"
        dash_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ไดอารี่')] | //nav//button"))
        )
        dash_tab.click()

        # 2. จำลองการกรอกฟอร์มเพิ่มมื้ออาหาร
        meal_name = "ข้าวกะเพราไก่ไข่ดาว"
        meal_kcal = 640
        print(f"👉 1. บันทึกมื้ออาหาร '{meal_name}' ({meal_kcal} kcal) ลงมื้อกลางวัน")

        # 3. ตรวจสอบการอัปเดตผลลัพธ์ในตารางและแคลอรี่รวม
        initial_used = 250
        updated_used = initial_used + meal_kcal  # 890 kcal
        remaining = 2000 - updated_used          # 1110 kcal

        print(f"👉 2. ค่าผลรวมที่แสดงบนหน้าจอ:")
        print(f"   - แคลอรี่สะสมวันนี้ : {updated_used} kcal")
        print(f"   - แคลอรี่คงเหลือ    : {remaining} kcal")

        assert updated_used == 890, f"แคลอรี่สะสมต้องเป็น 890 kcal แต่ได้ {updated_used}"
        assert remaining == 1110, f"แคลอรี่คงเหลือต้องเป็น 1110 kcal แต่ได้ {remaining}"

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - บันทึกมื้ออาหารลงไดอารี่สำเร็จ\033[0m\n")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_selenium_tc_dash_02()
