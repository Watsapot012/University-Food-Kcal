#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ตัวรันชุดทดสอบ Backend (Test Runner) สำหรับระบบ University Food Kcal
สามารถรันได้โดยตรงด้วยคำสั่ง:
    python backend/run_tests.py
    หรือ
    python run_tests.py (เมื่ออยู่ในโฟลเดอร์ backend)
"""

import sys
import os
import time
import unittest

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

# กำหนดเส้นทางโฟลเดอร์
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, '..'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def print_banner():
    print("\n" + "=" * 62)
    print("🧪  ชุดทดสอบระบบ University Food Kcal (Backend Test Suite)")
    print("    มหาวิทยาลัยราชภัฏนครปฐม (Nakhon Pathom Rajabhat University)")
    print("=" * 62 + "\n")
    sys.stdout.flush()

def run():
    print_banner()

    start_time = time.time()

    # โหลดชุดทดสอบจาก test_app.py
    loader = unittest.TestLoader()
    try:
        from test_app import (
            TestThaiEncodingAndSanitizer,
            TestNutritionFormulas,
            TestDatabaseSchemaIntegrity,
            TestFlaskEndpoints
        )
        suite = unittest.TestSuite()
        suite.addTests(loader.loadTestsFromTestCase(TestThaiEncodingAndSanitizer))
        suite.addTests(loader.loadTestsFromTestCase(TestNutritionFormulas))
        suite.addTests(loader.loadTestsFromTestCase(TestDatabaseSchemaIntegrity))
        suite.addTests(loader.loadTestsFromTestCase(TestFlaskEndpoints))
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการโหลดชุดทดสอบ: {e}")
        return 1

    print("📋 เริ่มดำเนินการทดสอบตามหมวดหมู่...")
    print("-" * 62)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    elapsed = round(time.time() - start_time, 3)

    print("\n" + "=" * 62)
    print("📊 สรุปผลการทดสอบ Backend (Summary):")
    print(f"   จำนวนการทดสอบทั้งหมด: {result.testsRun} รายการ")
    print(f"   เวลาที่ใช้:           {elapsed} วินาที")

    if result.wasSuccessful():
        print(f"   สถานะ:                ✅ ผ่านทั้งหมด 100% (PASSED) 🎉")
        print("=" * 62 + "\n")
        return 0
    else:
        print(f"   ข้อผิดพลาด (Errors):   {len(result.errors)}")
        print(f"   ไม่ผ่าน (Failures):    {len(result.failures)}")
        print(f"   สถานะ:                ❌ มีการทดสอบที่ไม่ผ่าน")
        print("=" * 62 + "\n")
        return 1

if __name__ == '__main__':
    exit_code = run()
    sys.exit(exit_code)
