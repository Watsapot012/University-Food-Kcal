#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Selenium Test Case ID : TC-FOOD-02
หน้าจอ       : หน้ารายการอาหาร (Food List Page)
ฟังก์ชัน      : กรองอาหารตามช่วงแคลอรี่ (Kcal Range Filter) ด้วย Selenium
ข้อมูลนำเข้า  : กำหนดช่วงแคลอรี่ Min: 200 kcal, Max: 450 kcal
ผลลัพธ์ที่คาดหวัง: แสดงเฉพาะเมนูอาหารที่แคลอรี่อยู่ในช่วง 200–450 kcal เท่านั้น
================================================================================
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, APP_URL, By, WebDriverWait, EC


def test_selenium_tc_food_02():
    print("=" * 70)
    print("🤖 Selenium Test: TC-FOOD-02 (หน้ารายการอาหาร - กรองช่วงแคลอรี่ด้วย WebDriver)")
    print("=" * 70)

    driver = get_driver()

    try:
        driver.get(APP_URL)

        # 1. คลิกแท็บ "เมนูอาหาร"
        food_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nav-link-foods"))
        )
        food_tab.click()

        # 2. ปรับการกรองช่วงแคลอรี่ Min=200, Max=450
        print("👉 1. ตั้งค่าการกรองช่วงแคลอรี่ Min: 200 kcal, Max: 450 kcal")
        min_kcal_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "kcal-min"))
        )
        max_kcal_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "kcal-max"))
        )
        min_kcal_input.send_keys("200")
        max_kcal_input.send_keys("450")

        # 3. ดึงการ์ดอาหารที่ผ่านการกรอง
        food_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".food-card, [data-testid='food-card'], div[data-id]"))
        )

        print(f"👉 2. ผลลัพธ์: ตรวจพบ {len(food_cards)} เมนูที่อยู่ในช่วง 200-450 kcal")
        for card in food_cards:
            kcal_str = card.get_attribute("data-kcal")
            assert kcal_str and kcal_str.isdigit(), "การ์ดอาหารต้องแสดงค่า data-kcal ที่ถูกต้อง"
            kcal = int(kcal_str)
            assert 200 <= kcal <= 450, f"ค่าแคลอรี่ {kcal} อยู่นอกช่วง 200-450 kcal"
            print(f"   🥗 {card.text}")

        assert len(food_cards) > 0, "ต้องพบอาหารที่อยู่ในช่วงแคลอรี่ที่กำหนด"

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - กรองช่วงแคลอรี่บนหน้าจอถูกต้อง\033[0m\n")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_selenium_tc_food_02()
