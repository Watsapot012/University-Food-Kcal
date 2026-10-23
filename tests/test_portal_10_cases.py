#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ไฟล์รวมการรันแบบทดสอบทั้งหมด: test_all_cases.py
(คล้าย test_portal_10_cases.py ที่รวมการรันทั้ง 10 Test Cases ของเว็บไซต์เรา)
================================================================================
"""

import subprocess
import sys
import os

from helpers import stop_local_app

TEST_FILES = [
    "test_01_TC_HOME_01_ค้นหาด่วน.py",
    "test_02_TC_HOME_02_ตัวชี้วัดสรุป.py",
    "test_03_TC_REST_01_แสดงร้านค้า.py",
    "test_04_TC_REST_02_กรองเมนูตามร้าน.py",
    "test_05_TC_FOOD_01_ค้นหาเมนูอาหาร.py",
    "test_06_TC_FOOD_02_กรองช่วงแคลอรี่.py",
    "test_07_TC_CUST_02_ปรับแต่งเพิ่มไข่ดาว.py",
    "test_08_TC_DASH_02_บันทึกมื้ออาหาร.py",
    "test_09_TC_PROF_01_คำนวณBMR_TDEE.py",
    "test_10_TC_AUTH_01_เข้าสู่ระบบ.py",
]


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Keep Thai and emoji output readable in Windows consoles using legacy encodings.
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

def run_all_tests():
    try:
        print("=" * 75)
        print("🚀 เริ่มต้นการรันแบบทดสอบ 10 Test Cases ประจำเว็บไซต์ University Food Kcal")
        print("=" * 75)

        passed_count = 0
        failed_count = 0
        test_options = [
            option for option in sys.argv[1:]
            if option in ("--browser", "--keep-open", "--no-keep-open")
        ]

        for idx, test_file_name in enumerate(TEST_FILES, 1):
            target_path = test_file_name
            if not os.path.exists(target_path):
                target_path = os.path.join(BASE_DIR, test_file_name)
            if not os.path.exists(target_path):
                print(f"\n[{idx}/10] ❌ ไม่พบไฟล์: {test_file_name}")
                failed_count += 1
                continue

            print(f"\n▶ กำลังรัน: [{idx}/10] {test_file_name} ...")
            command = [sys.executable, "-u", target_path, *test_options]
            proc = subprocess.run(command)

            if proc.returncode == 0:
                passed_count += 1
                print("  \033[92m✔ ผ่าน (PASS)\033[0m")
            else:
                failed_count += 1
                print(f"  \033[91m✖ ไม่ผ่าน (FAIL)\033[0m")

        print("\n" + "=" * 75)
        print("📊 สรุปผลการรัน Test Cases ทั้ง 10 เคส:")
        print("=" * 75)
        print(f"  การทดสอบทั้งหมด : {len(TEST_FILES)} ไฟล์")
        print(f"  \033[92mผ่าน (Passed)    : {passed_count} ไฟล์\033[0m")
        if failed_count > 0:
            print(f"  \033[91mไม่ผ่าน (Failed)  : {failed_count} ไฟล์\033[0m")
        else:
            print("  \033[92mสถานะ            : ผ่านครบ 100% ทุกไฟล์แบบทดสอบ! 🎉\033[0m")
        print("=" * 75 + "\n")
        return 0 if failed_count == 0 else 1
    finally:
        stop_local_app()

run_all_cases = run_all_tests

if __name__ == "__main__":
    sys.exit(run_all_tests())
