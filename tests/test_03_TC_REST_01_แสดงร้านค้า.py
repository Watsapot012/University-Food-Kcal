#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Selenium Test Case ID : TC-REST-01
หน้าจอ       : หน้าร้านอาหาร (Restaurants Page)
ฟังก์ชัน      : คลิกเข้าสู่แท็บร้านอาหารและแสดงรายชื่อร้านค้า (List All Restaurants)
ข้อมูลนำเข้า  : คลิกปุ่มเมนู "ร้านอาหาร" บน Navbar
ผลลัพธ์ที่คาดหวัง: แสดงรายชื่อร้านค้าทั้งหมดใน มรภ.นครปฐม พร้อมสถานที่ตั้งบนหน้าเว็บ
================================================================================
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, APP_URL, By, WebDriverWait, EC


def test_selenium_tc_rest_01():
    print("=" * 70)
    print("🤖 Selenium Test: TC-REST-01 (หน้าร้านอาหาร - แสดงรายชื่อร้านค้าด้วย WebDriver)")
    print("=" * 70)

    print(f"👉 1. เปิดเบราว์เซอร์ไปที่: {APP_URL}")
    driver = get_driver(headless=True)

    try:
        driver.get(APP_URL)

        # 2. คลิกปุ่มแท็บ 'ร้านอาหาร' บน Navbar
        print("👉 2. ค้นหาปุ่มนำทาง (Navigation Button) 'ร้านอาหาร' และสั่ง click()")
        nav_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ร้านอาหาร')] | //nav//button"))
        )
        nav_button.click()

        # 3. รอให้การ์ดร้านอาหารปรากฏขึ้นมา
        print("👉 3. รอ Web Elements รายการร้านอาหารแสดงผล")
        restaurant_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".restaurant-card, [data-testid='restaurant-card'], div[data-id]"))
        )

        print(f"👉 4. พบร้านอาหารทั้งหมด: {len(restaurant_cards)} ร้าน")
        for card in restaurant_cards[:4]:
            print(f"   🏢 {card.text}")

        # 4. Assertions ตรวจสอบ
        assert len(restaurant_cards) >= 4, f"ต้องพบร้านอาหารอย่างน้อย 4 ร้าน แต่พบ {len(restaurant_cards)}"

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - นำทางไปหน้าร้านอาหารและแสดงผลร้านค้าครบถ้วน\033[0m\n")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_selenium_tc_rest_01()
