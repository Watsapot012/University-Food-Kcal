#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 10: ทดสอบผู้ดูแลระบบ (Admin) เปลี่ยนแปลงข้อมูลร้านค้า / สถิติระบบ
ฟังก์ชัน: PUT /api/restaurants/:id และ GET /api/stats
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import ApiClient

def test_admin_change_restaurant():
    """ทดสอบแอดมินเปลี่ยนข้อมูลร้านค้า และระบบคำนวณสถิติภาพรวม"""
    client = ApiClient()

    # 1. แอดมินแก้ไขข้อมูลร้านค้าที่ 1
    new_info = {
        "name": "ร้านอาหารตามสั่งราชภัฏ (ปรับปรุงใหม่)",
        "open_hours": "07:30 - 18:30 น.",
        "description": "อาหารสด สะอาด ถูกหลักโภชนาการ นครปฐม"
    }
    status, response = client.put("/restaurants/1", data=new_info)
    print(f"\n[Test 10.1] Admin เปลี่ยนข้อมูลร้าน: PUT /api/restaurants/1")
    print(f"  Response Status: {status}")
    print(f"  Updated Name: {response.get('name')}")
    print(f"  Updated Hours: {response.get('open_hours')}")

    assert status == 200, f"คาดหวัง Status 200 แต่ได้ {status}"
    assert response["name"] == new_info["name"], "ชื่อร้านต้องเปลี่ยนตามที่ระบุ"

    # 2. ตรวจสอบสถิติระบบ Admin Stats
    status_stats, stats = client.get("/stats")
    print(f"\n[Test 10.2] ตรวจสอบสถิติระบบ: GET /api/stats")
    print(f"  Total Restaurants: {stats.get('total_restaurants')}")
    print(f"  Total Foods: {stats.get('total_foods')}")
    print(f"  Average Kcal: {stats.get('avg_kcal')}")

    assert status_stats == 200, f"คาดหวัง Status 200 แต่ได้ {status_stats}"
    assert stats.get("total_restaurants", 0) > 0, "ต้องมีร้านอาหารในสถิติ"
    assert stats.get("avg_kcal", 0) > 0, "ค่าเฉลี่ยแคลอรี่ต้องมากกว่า 0"

    print("  \033[92m✔ ผ่านการทดสอบ: ผู้ดูแลระบบเปลี่ยนแปลงข้อมูลและคำนวณสถิติระบบสำเร็จ\033[0m")
    return True

if __name__ == "__main__":
    test_admin_change_restaurant()
