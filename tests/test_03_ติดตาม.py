#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 03: ทดสอบระบบติดตามแคลอรี่และสารอาหารประจำวัน (Daily Tracking & BMR/TDEE)
ฟังก์ชัน: GET /api/logs และ GET /api/profile
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import ApiClient, load_state

def test_tracking_daily_kcal():
    """ทดสอบการติดตามข้อมูลอาหารที่กินและผลรวมแคลอรี่สะสม"""
    client = ApiClient()
    state = load_state()
    user_id = state.get("userId", 1)

    # 1. ติดตามรายการอาหารและแคลอรี่รวม
    status, logs_res = client.get(f"/logs?userId={user_id}")
    print(f"\n[Test 03] GET /api/logs?userId={user_id}")
    print(f"  Response Status: {status}")
    print(f"  Total Calories: {logs_res.get('totalCalories')}")
    print(f"  Meals Count: {len(logs_res.get('meals', []))}")

    assert status == 200, f"คาดหวัง Status 200 แต่ได้ {status}"
    assert "meals" in logs_res, "ต้องมีรายการ meals ในการติดตาม"
    assert "totalCalories" in logs_res, "ต้องมี totalCalories"
    assert logs_res["totalCalories"] > 0, "แคลอรี่รวมต้องมากกว่า 0"

    # 2. ติดตามเป้าหมาย TDEE จาก Profile
    status_prof, prof_res = client.get(f"/profile?userId={user_id}")
    assert status_prof == 200, f"คาดหวัง Profile Status 200 แต่ได้ {status_prof}"
    assert "bmr" in prof_res and "tdee" in prof_res, "ต้องมีเป้าหมาย BMR และ TDEE เพื่อติดตาม"

    print(f"  User Target TDEE: {prof_res.get('tdee')} kcal (BMR: {prof_res.get('bmr')} kcal)")
    print("  \033[92m✔ ผ่านการทดสอบ: ติดตามบันทึกแคลอรี่และสารอาหารประจำวันถูกต้องสมบูรณ์\033[0m")
    return True

if __name__ == "__main__":
    test_tracking_daily_kcal()
