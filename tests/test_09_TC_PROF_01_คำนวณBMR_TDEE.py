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

from helpers import get_driver, quit_driver, APP_URL, By, WebDriverWait, EC
from selenium.webdriver.support.ui import Select


def test_selenium_tc_prof_01():
    print("=" * 70)
    print("🤖 Selenium Test: TC-PROF-01 (โปรไฟล์ - กรอกฟอร์มคำนวณ BMR & TDEE)")
    print("=" * 70)

    driver = get_driver()

    try:
        driver.get(APP_URL)

        # Open the profile page from the user menu.
        driver.find_element(By.ID, "user-profile-menu-btn").click()
        prof_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'โปรไฟล์ & BMR/TDEE')]"))
        )
        prof_tab.click()

        # Enter the scenario values in the actual profile form.
        weight = 65.0
        height = 175.0
        age = 21
        gender = 'male'
        activity = 1.55

        number_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='number']")
        assert len(number_inputs) >= 4, "ต้องพบช่องกรอกน้ำหนัก ส่วนสูง อายุ และเป้าหมายแคลอรี่"
        for field, value in zip(number_inputs[:3], (weight, height, age)):
            field.clear()
            field.send_keys(str(value))
        Select(driver.find_element(By.TAG_NAME, "select")).select_by_value(str(activity))

        print(f"👉 1. กรอกข้อมูลจริงบนหน้าโปรไฟล์: เพศ={gender}, นน.={weight}กก., สส.={height}ซม., อายุ={age}ปี, กิจกรรม={activity}")

        # Calculate using the page's TDEE button without saving a profile.
        expected_bmr = round((10 * weight) + (6.25 * height) - (5 * age) + 5) # 1644
        expected_tdee = round(expected_bmr * activity)                         # 2548
        driver.find_element(By.XPATH, "//button[contains(., 'ตั้งตาม TDEE')]").click()

        result_cards = WebDriverWait(driver, 10).until(
            lambda current_driver: [
                card for card in current_driver.find_elements(By.CSS_SELECTOR, "div.glass-inner")
                if "BMR (" in card.text or "TDEE (" in card.text
            ]
        )
        bmr_card = next((card for card in result_cards if "BMR (" in card.text), None)
        tdee_card = next((card for card in result_cards if "TDEE (" in card.text), None)
        assert bmr_card and tdee_card, "ไม่พบการ์ดผลลัพธ์ BMR/TDEE บนหน้าเว็บ"
        actual_bmr = bmr_card.find_element(By.TAG_NAME, "span").text
        actual_tdee = tdee_card.find_element(By.TAG_NAME, "span").text

        print("👉 2. ผลลัพธ์ที่อ่านจากหน้าเว็บจริง:")
        print(f"   - ค่า BMR  : {actual_bmr} kcal/วัน")
        print(f"   - ค่า TDEE : {actual_tdee} kcal/วัน")

        assert int(actual_bmr) == expected_bmr, f"BMR ต้องเป็น {expected_bmr} kcal แต่ได้ {actual_bmr}"
        assert int(actual_tdee) == expected_tdee, f"TDEE ต้องเป็น {expected_tdee} kcal แต่ได้ {actual_tdee}"

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - ตรวจสอบฟอร์มสุขภาพและคำนวณ BMR/TDEE สำเร็จ\033[0m\n")

    finally:
        quit_driver(driver)


if __name__ == "__main__":
    test_selenium_tc_prof_01()
