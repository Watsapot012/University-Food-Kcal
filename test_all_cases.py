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
import glob
import os

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


def run_all_tests():
    print("=" * 75)
    print("🚀 เริ่มต้นการรันแบบทดสอบ 10 Test Cases ประจำเว็บไซต์ University Food Kcal")
    print("=" * 75)

    passed_count = 0
    failed_count = 0

    for idx, test_file in enumerate(TEST_FILES, 1):
        if not os.path.exists(test_file):
            print(f"\n[{idx}/10] ❌ ไม่พบไฟล์: {test_file}")
            failed_count += 1
            continue

        print(f"\n▶ กำลังรัน: [{idx}/10] {test_file} ...")
        proc = subprocess.run([sys.executable, test_file], capture_output=True, text=True, encoding="utf-8")

        if proc.returncode == 0:
            passed_count += 1
            # พิมพ์เฉพาะบรรทัดสรุปของแต่ละไฟล์
            lines = [line for line in proc.stdout.split("\n") if "PASS" in line or "ผ่าน" in line]
            status_line = lines[-1] if lines else "ผ่านการทดสอบ (PASS)"
            print(f"  \033[92m✔ {status_line.strip()}\033[0m")
        else:
            failed_count += 1
            print(f"  \033[91m✖ ไม่ผ่าน (FAIL)\033[0m")
            print(proc.stderr or proc.stdout)

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


if __name__ == "__main__":
    run_all_tests()
