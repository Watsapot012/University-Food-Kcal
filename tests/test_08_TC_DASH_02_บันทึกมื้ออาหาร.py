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

from helpers import get_driver, quit_driver, APP_URL, By, WebDriverWait, EC


def test_selenium_tc_dash_02():
    print("=" * 70)
    print("🤖 Selenium Test: TC-DASH-02 (ไดอารี่ - บันทึกมื้ออาหารลงตารางด้วย WebDriver)")
    print("=" * 70)

    driver = get_driver()

    try:
        driver.get(APP_URL)

        # 1. Navigate to the daily dashboard.
        dash_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nav-link-dashboard"))
        )
        dash_tab.click()

        # 2. Record the current calorie total, then add a meal through the form.
        total_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.text-3xl"))
        )
        initial_total = int(total_element.text)
        meal_name = "ทดสอบข้าวกะเพราไก่ไข่ดาว"
        meal_kcal = 640
        driver.find_element(By.XPATH, "//button[contains(., 'เพิ่มรายการอาหาร')]").click()
        driver.find_element(By.CSS_SELECTOR, "input[placeholder*='ข้าวกะเพรา']").send_keys(meal_name)
        driver.find_element(By.CSS_SELECTOR, "input[placeholder*='450']").send_keys(str(meal_kcal))
        driver.find_element(By.XPATH, "//button[@type='submit' and contains(., 'บันทึกอาหาร')]").click()

        # 3. Verify the new meal appears and the actual total increases.
        meal_row = WebDriverWait(driver, 10).until(
            lambda current_driver: current_driver.find_element(
                By.XPATH,
                f"//div[contains(@class, 'font-bold') and normalize-space()='{meal_name}']",
            )
        )
        updated_total = int(driver.find_element(By.CSS_SELECTOR, "span.text-3xl").text)
        expected_total = initial_total + meal_kcal

        print(f"👉 1. เพิ่มรายการบนหน้าเว็บ: {meal_row.text} ({meal_kcal} kcal)")
        print(f"👉 2. แคลอรี่สะสมจริง: {initial_total} → {updated_total} kcal")
        assert meal_name in meal_row.text, "รายการอาหารใหม่ต้องแสดงในรายการประจำวัน"
        assert updated_total == expected_total, (
            f"แคลอรี่สะสมต้องเป็น {expected_total} kcal แต่ได้ {updated_total}"
        )

        # Remove the test entry so repeated runs do not pollute the daily log.
        delete_button = meal_row.find_element(
            By.XPATH,
            "ancestor::div[contains(@class, 'py-4')][1]//button[@title='ลบรายการนี้']",
        )
        delete_button.click()

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - บันทึกมื้ออาหารลงไดอารี่สำเร็จ\033[0m\n")

    finally:
        quit_driver(driver)


if __name__ == "__main__":
    test_selenium_tc_dash_02()
