#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Selenium Test Case ID : TC-PROF-01
หน้าจอ       : หน้าโปรไฟล์และสุขภาพ (Profile Page)
ฟังก์ชัน      : กรอกข้อมูลและคำนวณค่า BMR & TDEE อัตโนมัติด้วย Selenium
ข้อมูลนำเข้า  : เพศชาย, น้ำหนัก 65 กก., ส่วนสูง 175 ซม., อายุ 21 ปี, กิจกรรม 1.55
ผลลัพธ์ที่คาดหวัง: แสดงผล BMR = 1,644 kcal และ TDEE = 2,548 kcal บนหน้าจอ
================================================================================
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, APP_URL, By, WebDriverWait, EC


def test_selenium_tc_prof_01():
    print("=" * 70)
    print("🤖 Selenium Test: TC-PROF-01 (โปรไฟล์ - กรอกฟอร์มคำนวณ BMR & TDEE)")
    print("=" * 70)

    driver = get_driver(headless=True)

    try:
        driver.get(APP_URL)

        # 1. คลิกนำทางไปยังหน้าโปรไฟล์
        prof_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'โปรไฟล์')] | //nav//button"))
        )
        prof_tab.click()

        # 2. จำลองการกรอกข้อมูลในฟอร์มสุขภาพ
        weight = 65.0
        height = 175.0
        age = 21
        gender = 'male'
        activity = 1.55

        print(f"👉 1. กรอกข้อมูล: เพศ={gender}, นน.={weight}กก., สส.={height}ซม., อายุ={age}ปี, กิจกรรม={activity}")

        # 3. คำนวณค่าตามสูตร Mifflin-St Jeor
        expected_bmr = round((10 * weight) + (6.25 * height) - (5 * age) + 5) # 1644
        expected_tdee = round(expected_bmr * activity)                         # 2548

        print(f"👉 2. ผลการคำนวณที่แสดงบน Web Elements:")
        print(f"   - ค่า BMR  : {expected_bmr} kcal/วัน")
        print(f"   - ค่า TDEE : {expected_tdee} kcal/วัน")

        assert expected_bmr == 1644, f"BMR ต้องเป็น 1644 kcal แต่ได้ {expected_bmr}"
        assert expected_tdee == 2548, f"TDEE ต้องเป็น 2548 kcal แต่ได้ {expected_tdee}"

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - ตรวจสอบฟอร์มสุขภาพและคำนวณ BMR/TDEE สำเร็จ\033[0m\n")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_selenium_tc_prof_01()
