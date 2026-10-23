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
import re
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, quit_driver, APP_URL, By, WebDriverWait, EC
from selenium.webdriver.support.ui import Select


def test_selenium_tc_cust_02():
    print("=" * 70)
    print("🤖 Selenium Test: TC-CUST-02 (ปรับแต่งอาหาร - เพิ่มไข่ดาวคำนวณ Real-time)")
    print("=" * 70)

    driver = get_driver()

    try:
        driver.get(APP_URL)

        # 1. Navigate to the meal customizer and read the selected dish's calories.
        customizer_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nav-link-customizer"))
        )
        customizer_tab.click()

        menu_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "select"))
        )
        selected_menu = Select(menu_select).first_selected_option.text
        base_match = re.search(r"\((\d+)\s*kcal\)", selected_menu)
        assert base_match, f"อ่านค่าแคลอรี่จากเมนูที่เลือกไม่ได้: {selected_menu}"
        base_kcal = int(base_match.group(1))
        addon_kcal = 90

        print(f"👉 1. เมนูตั้งต้น: {selected_menu}")
        print(f"👉 2. เลือกท็อปปิ้ง 'ไข่ดาว (+{addon_kcal} kcal)' บนหน้าจอ")
        fried_egg_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class, 'cursor-pointer')][.//div[normalize-space()='ไข่ดาว']]",
            ))
        )
        fried_egg_option.click()

        expected_kcal = base_kcal + addon_kcal
        total_kcal = WebDriverWait(driver, 10).until(
            lambda current_driver: current_driver.find_element(
                By.XPATH,
                "//*[text()='แคลอรี่รวมหลังปรับแต่ง']/following-sibling::div//span[contains(@class, 'text-5xl')]",
            )
        ).text
        print(f"👉 3. ค่าบนหน้าจอหลังเลือกไข่ดาว: {total_kcal} kcal (คาดหวัง {expected_kcal} kcal)")
        assert int(total_kcal) == expected_kcal, (
            f"ค่าแคลอรี่รวมบนหน้าจอต้องเป็น {expected_kcal} kcal แต่ได้ {total_kcal}"
        )

        print("\n\033[92m✔ ผลการทดสอบ (Selenium): ผ่าน (PASS) - คำนวณแคลอรี่สุทธิใหม่ Real-time สำเร็จ\033[0m\n")

    finally:
        quit_driver(driver)


if __name__ == "__main__":
    test_selenium_tc_cust_02()
