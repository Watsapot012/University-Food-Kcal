#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Selenium Test Case ID : TC-HOME-01
หน้าจอ       : หน้าแรก (Home Page)
ฟังก์ชัน      : ค้นหาด่วน (Quick Search Bar) ด้วย Selenium WebDriver
ข้อมูลนำเข้า  : พิมพ์คำว่า "กะเพรา" และกดปุ่มค้นหา/Enter
ผลลัพธ์ที่คาดหวัง: เบราว์เซอร์พุ่งไปหน้ารายการอาหาร และแสดงเฉพาะเมนูกะเพรา
================================================================================
"""

import os
import sys

# เพิ่มโฟลเดอร์ tests เข้า sys.path
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, quit_driver, APP_URL, By, Keys, WebDriverWait, EC


def test_selenium_tc_home_01():
    print("=" * 70)
    print("🤖 Selenium Test: TC-HOME-01 (หน้าแรก - ค้นหาด่วนด้วย WebDriver)")
    print("=" * 70)

    # 1. เริ่มต้นเปิดเบราว์เซอร์ผ่าน Selenium WebDriver
    print(f"👉 1. เปิดเบราว์เซอร์ไปยัง URL: {APP_URL}")
    driver = get_driver()

    try:
        driver.get(APP_URL)

        # 2. ค้นหาช่อง Search input บนหน้าแรก
        print("👉 2. ค้นหา Web Element กล่องค้นหา (Search Input Bar)")
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='ค้นหา']"))
        )

        # 3. ส่งคำค้นหา "กะเพรา" และกดปุ่ม Enter
        search_keyword = "กะเพรา"
        print(f"👉 3. พิมพ์ข้อความ '{search_keyword}' ลงในกล่องค้นหาและกด Send Keys (RETURN)")
        search_input.clear()
        search_input.send_keys(search_keyword)
        search_input.send_keys(Keys.RETURN)

        # 4. รอให้รายการอาหารปรากฏขึ้นมาบนหน้าเว็บ
        food_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".food-card, [data-testid='food-card'], div[data-id]"))
        )

        print(f"👉 4. ผลลัพธ์: ตรวจพบ {len(food_cards)} การ์ดเมนูอาหารบนหน้าเว็บ")
        for card in food_cards[:5]:
            print(f"   - {card.text}")

        # 5. Assertions ตรวจสอบความถูกต้อง
        assert len(food_cards) > 0, "ต้องพบการ์ดเมนูอาหารอย่างน้อย 1 รายการ"
        assert all(search_keyword in card.text for card in food_cards), (
            f"เมนูทุกใบต้องมีคำว่า '{search_keyword}' หลังกรอง"
        )

        print(f"\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - ค้นหา '{search_keyword}' และแสดงผลบนเบราว์เซอร์ถูกต้อง\033[0m\n")

    finally:
        quit_driver(driver)


if __name__ == "__main__":
    test_selenium_tc_home_01()
