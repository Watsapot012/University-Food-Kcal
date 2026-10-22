#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ชุดทดสอบรวม 10 Test Cases (Portal Test Runner)
ระบบวิเคราะห์แคลอรี่อาหาร มหาวิทยาลัยราชภัฏนครปฐม (University Food Kcal)

รันด้วยคำสั่ง:
    python tests/test_portal_10_cases.py
"""

import os
import sys
import time

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

# นำเข้าฟังก์ชันทดสอบทั้ง 10 เคส
from test_01_login import test_login_success
import importlib

# โหลดโมดูลภาษาไทยแบบไดนามิกเพื่อความเข้ากันได้ทุกระบบ
test_02 = importlib.import_module("test_02_กรอกแบบฟอร์มและกดส่ง")
test_03 = importlib.import_module("test_03_ติดตาม")
test_04 = importlib.import_module("test_04_login_ไม่ได้")
test_05 = importlib.import_module("test_05_กรอกฟอร์มผิด")
test_06 = importlib.import_module("test_06_admin_แก้ไข")
test_07 = importlib.import_module("test_07_ลบ")
test_08 = importlib.import_module("test_08_กรอกติดตามผิด")
test_09 = importlib.import_module("test_09_admin_ลบ")
test_10 = importlib.import_module("test_10_admin_เปลี่ยน")

TEST_CASES = [
    ("TC-01", "test_01_login", "ทดสอบการเข้าสู่ระบบสำเร็จ (Login Success)", test_login_success),
    ("TC-02", "test_02_กรอกแบบฟอร์มและกดส่ง", "ทดสอบกรอกแบบฟอร์มบันทึกอาหารและกดส่ง", test_02.test_submit_meal_log),
    ("TC-03", "test_03_ติดตาม", "ทดสอบระบบติดตามแคลอรี่และสารอาหารประจำวัน", test_03.test_tracking_daily_kcal),
    ("TC-04", "test_04_login_ไม่ได้", "ทดสอบกรณีรหัสผ่านผิด / Login ไม่ผ่าน", test_04.test_login_failed_wrong_password),
    ("TC-05", "test_05_กรอกฟอร์มผิด", "ทดสอบกรณีส่งแบบฟอร์มข้อมูลผิดพลาด/ไม่ครบ", test_05.test_form_validation_errors),
    ("TC-06", "test_06_admin_แก้ไข", "ทดสอบ Admin แก้ไขข้อมูลอาหารและสารอาหาร", test_06.test_admin_edit_food),
    ("TC-07", "test_07_ลบ", "ทดสอบผู้ใช้ลบรายการอาหารออกจากบันทึก", test_07.test_delete_user_log),
    ("TC-08", "test_08_กรอกติดตามผิด", "ทดสอบกรณีค้นหา/ติดตามข้อมูลผิดพลาด (404 Not Found)", test_08.test_track_invalid_not_found),
    ("TC-09", "test_09_admin_ลบ", "ทดสอบ Admin ลบเมนูอาหารออกจากฐานข้อมูล", test_09.test_admin_delete_food),
    ("TC-10", "test_10_admin_เปลี่ยน", "ทดสอบ Admin เปลี่ยนแปลงข้อมูลร้านค้าและสถิติ", test_10.test_admin_change_restaurant),
]

def run_all_cases():
    print("\n" + "=" * 70)
    print("🚀  ชุดทดสอบรวม 10 Test Cases (University Food Kcal - NPRU)")
    print("=" * 70)

    results = []
    start_total = time.time()

    for tc_id, file_name, desc, test_fn in TEST_CASES:
        start = time.time()
        print(f"\n▶ กำลังรัน {tc_id}: {file_name}.py ({desc})...")
        try:
            test_fn()
            duration = round((time.time() - start) * 1000, 1)
            results.append((tc_id, file_name, desc, "PASS", duration, None))
        except Exception as e:
            duration = round((time.time() - start) * 1000, 1)
            results.append((tc_id, file_name, desc, "FAIL", duration, str(e)))
            print(f"  \033[91m✖ ไม่ผ่าน: {e}\033[0m")

    total_time = round(time.time() - start_total, 3)

    print("\n" + "=" * 70)
    print("📊 ตารางสรุปผลการทดสอบทั้งหมด 10 Test Cases:")
    print("=" * 70)
    print(f"{'รหัส':<7} | {'ชื่อไฟล์':<30} | {'สถานะ':<8} | {'เวลา (ms)':<10}")
    print("-" * 70)

    passed_count = sum(1 for r in results if r[3] == "PASS")
    for tc_id, file_name, desc, status, duration, err in results:
        status_color = "\033[92m✔ PASS\033[0m" if status == "PASS" else "\033[91m✖ FAIL\033[0m"
        print(f"{tc_id:<7} | {file_name:<30} | {status_color:<17} | {duration:<10} ms")

    print("-" * 70)
    print(f"ผลลัพธ์: ผ่าน {passed_count}/{len(TEST_CASES)} เคส ({passed_count/len(TEST_CASES)*100:.0f}%) | เวลาที่ใช้: {total_time} วินาที")

    if passed_count == len(TEST_CASES):
        print("\033[92m🎉 ผ่านการทดสอบครบทั้ง 10 เคสอย่างสมบูรณ์ 100%!\033[0m")
        print("=" * 70 + "\n")
        return 0
    else:
        print("\033[91m⚠️ มีบางเคสไม่ผ่าน กรุณาตรวจสอบรายละเอียดด้านบน\033[0m")
        print("=" * 70 + "\n")
        return 1

if __name__ == "__main__":
    code = run_all_cases()
    sys.exit(code)
