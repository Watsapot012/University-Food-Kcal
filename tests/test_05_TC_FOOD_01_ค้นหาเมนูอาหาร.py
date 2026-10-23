#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Selenium Test Case ID : TC-FOOD-01
หน้าจอ       : หน้ารายการอาหาร (Food List Page)
ฟังก์ชัน      : ค้นหาชื่ออาหารด้วยคีย์เวิร์ด (Search Food by Keyword) ด้วย Selenium
ข้อมูลนำเข้า  : พิมพ์คำว่า "ต้มยำ" ในช่องค้นหาหน้ารายการอาหาร
ผลลัพธ์ที่คาดหวัง: กรองรายการอาหารเหลือเฉพาะเมนูก๋วยเตี๋ยวต้มยำ
================================================================================
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, APP_URL, By, Keys, WebDriverWait, EC


def test_selenium_tc_food_01():
    print("=" * 70)
    print("🤖 Selenium Test: TC-FOOD-01 (หน้ารายการอาหาร - ค้นหา 'ต้มยำ' ด้วย WebDriver)")
    print("=" * 70)

    driver = get_driver()

    try:
        driver.get(APP_URL)

        # 1. คลิกแท็บ "เมนูอาหาร"
        food_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nav-link-foods"))
        )
        food_tab.click()

        # 2. ค้นหาช่องค้นหาในหน้ารายการอาหาร
        print("👉 1. ส่งคำค้นหา 'ต้มยำ' ในกล่องค้นหาอาหาร")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='ค้นหา']"))
        )
        search_box.clear()
        search_box.send_keys("ต้มยำ")
        search_box.send_keys(Keys.RETURN)

        # 3. ตรวจสอบผลลัพธ์การค้นหา
        food_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".food-card, [data-testid='food-card'], div[data-id]"))
        )

        matched_cards = [c for c in food_cards if "ต้มยำ" in c.text]
        print(f"👉 2. พบเมนูต้มยำทั้งหมด: {len(matched_cards)} รายการ")
        for c in matched_cards:
            print(f"   🍲 {c.text}")

        assert len(matched_cards) > 0, "ต้องพบเมนูต้มยำอย่างน้อย 1 รายการ"
        assert len(matched_cards) == len(food_cards), "ผลลัพธ์ทุกใบต้องตรงกับคำค้นหา 'ต้มยำ'"

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - กรองเมนูต้มยำตามคีย์เวิร์ดสำเร็จ\033[0m\n")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_selenium_tc_food_01()
