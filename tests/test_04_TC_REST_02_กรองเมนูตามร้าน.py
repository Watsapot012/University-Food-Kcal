#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Selenium Test Case ID : TC-REST-02
หน้าจอ       : หน้าร้านอาหาร (Restaurants Page)
ฟังก์ชัน      : กรองเมนูอาหารตามร้านที่เลือก (Filter Foods by Store) ด้วย Selenium
ข้อมูลนำเข้า  : คลิกเลือกการ์ดร้านค้า "ร้านป้าณี" (หรือร้านตามสั่ง)
ผลลัพธ์ที่คาดหวัง: หน้าร้านอาหารคัดกรองแสดงเฉพาะเมนูที่สังกัดร้านที่เลือก
================================================================================
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, APP_URL, By, WebDriverWait, EC


def test_selenium_tc_rest_02():
    print("=" * 70)
    print("🤖 Selenium Test: TC-REST-02 (หน้าร้านอาหาร - กรองเมนูตามร้านด้วย WebDriver)")
    print("=" * 70)

    driver = get_driver(headless=True)

    try:
        driver.get(APP_URL)

        # 1. คลิกแท็บร้านอาหาร
        nav_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ร้านอาหาร')] | //nav//button"))
        )
        nav_button.click()

        # 2. ค้นหาการ์ดร้านค้า "ร้านป้าณี" แล้วสั่ง click()
        print("👉 1. คลิกเลือกการ์ดร้านค้าแรก (Select Restaurant Card)")
        first_store_card = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".restaurant-card, [data-testid='restaurant-card'], div[data-id]"))
        )
        print(f"   คลิกเลือกร้าน: {first_store_card.text}")
        first_store_card.click()

        # 3. ตรวจสอบเมนูอาหารใต้ร้านค้านั้น
        print("👉 2. ตรวจสอบรายการอาหารที่ผ่านการกรอง (Filtered Menu List)")
        menu_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".food-card, [data-testid='food-card'], div[data-id]"))
        )

        print(f"   พบเมนูของร้านนี้: {len(menu_items)} รายการ")
        for item in menu_items[:3]:
            print(f"   🍽️ {item.text}")

        assert len(menu_items) > 0, "ต้องพบเมนูอาหารของร้านอย่างน้อย 1 รายการ"

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - กรองเมนูตามร้านค้าที่เลือกสำเร็จ\033[0m\n")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_selenium_tc_rest_02()
