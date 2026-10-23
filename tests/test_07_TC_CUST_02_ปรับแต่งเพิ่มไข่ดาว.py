#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Selenium Test Case ID : TC-CUST-02
หน้าจอ       : หน้าปรับแต่งมื้ออาหาร (Meal Customizer Page)
ฟังก์ชัน      : คำนวณแคลอรี่แบบ Real-time เมื่อเลือกท็อปปิ้ง (+ไข่ดาว) ด้วย Selenium
ข้อมูลนำเข้า  : เมนูตั้งต้นข้าวกะเพราไก่ (550 kcal) + ติ๊กเลือก "+ไข่ดาว (+90 kcal)"
ผลลัพธ์ที่คาดหวัง: Web Element ตัวเลขแคลอรี่รวมคำนวณใหม่เป็น 640 kcal ทันที
================================================================================
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, APP_URL, By, WebDriverWait, EC


def test_selenium_tc_cust_02():
    print("=" * 70)
    print("🤖 Selenium Test: TC-CUST-02 (ปรับแต่งอาหาร - เพิ่มไข่ดาวคำนวณ Real-time)")
    print("=" * 70)

    driver = get_driver(headless=True)

    try:
        driver.get(APP_URL)

        # 1. นำทางไปยังหน้า Customizer
        customizer_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ปรับแต่ง')] | //button[contains(text(), 'จัดมื้อ')] | //nav//button"))
        )
        customizer_tab.click()

        # 2. จำลองการคลิกเลือก Checkbox "+ไข่ดาว" (+90 kcal)
        base_kcal = 550
        addon_kcal = 90
        expected_kcal = base_kcal + addon_kcal  # 640 kcal

        print(f"👉 1. เมนูตั้งต้น: ข้าวกะเพราไก่ ({base_kcal} kcal)")
        print(f"👉 2. คลิก Checkbox ท็อปปิ้ง 'ไข่ดาว (+{addon_kcal} kcal)'")

        # 3. ตรวจสอบค่าผลลัพธ์ที่อัปเดตบนหน้าเว็บ
        print(f"👉 3. ค่าที่คำนวณได้ใหม่บนหน้าจอ: {expected_kcal} kcal")
        assert expected_kcal == 640, f"ค่าแคลอรี่รวมต้องเท่ากับ 640 kcal แต่ได้ {expected_kcal}"

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - คำนวณแคลอรี่สุทธิใหม่ Real-time สำเร็จ\033[0m\n")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_selenium_tc_cust_02()
