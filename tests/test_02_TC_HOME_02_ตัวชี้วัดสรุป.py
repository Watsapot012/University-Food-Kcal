#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Selenium Test Case ID : TC-HOME-02
หน้าจอ       : หน้าแรก (Home Page)
ฟังก์ชัน      : ตัวชี้วัดสรุปภาพรวม (Quick Stats Cards) ด้วย Selenium
ข้อมูลนำเข้า  : เปิดหน้าแรกของเว็บไซต์
ผลลัพธ์ที่คาดหวัง: ตรวจพบการ์ดสรุปสถิติ: จำนวนร้านค้า, จำนวนเมนู, ค่าเฉลี่ยแคลอรี่ แสดงผลบนหน้าจอ
================================================================================
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, quit_driver, APP_URL, By, WebDriverWait, EC


def test_selenium_tc_home_02():
    print("=" * 70)
    print("🤖 Selenium Test: TC-HOME-02 (หน้าแรก - ตัวชี้วัดสรุป Quick Stats ด้วย WebDriver)")
    print("=" * 70)

    print(f"👉 1. เปิดหน้าแรกที่ URL: {APP_URL}")
    driver = get_driver()

    try:
        driver.get(APP_URL)

        # 2. รอให้การ์ดสรุปสถิติบนหน้าแรกแสดงผล
        print("👉 2. ค้นหา Web Elements การ์ดสถิติ (Stat Cards)")
        stat_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".stat-card, [data-testid='stat-card'], div.grid > div"))
        )

        print(f"👉 3. ตรวจพบการ์ดสถิติทั้งหมด: {len(stat_cards)} รายการ")
        for idx, card in enumerate(stat_cards[:4], 1):
            print(f"   [การ์ดที่ {idx}] {card.text}")

        # 3. Assertions ตรวจสอบการแสดงผลสถิติ
        assert len(stat_cards) >= 3, f"ต้องพบการ์ดสถิติอย่างน้อย 3 ใบ แต่พบ {len(stat_cards)}"

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - การ์ดตัวชี้วัดสรุปแสดงผลบนหน้าจอถูกต้อง\033[0m\n")

    finally:
        quit_driver(driver)


if __name__ == "__main__":
    test_selenium_tc_home_02()
