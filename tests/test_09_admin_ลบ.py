#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 09: ทดสอบผู้ดูแลระบบ (Admin) ลบข้อมูลเมนูอาหารออกจากระบบ
ฟังก์ชัน: DELETE /api/foods/:id
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import ApiClient

def test_admin_delete_food():
    """ทดสอบแอดมินลบเมนูอาหารออกจากฐานข้อมูล"""
    client = ApiClient()

    # 1. แอดมินสร้างเมนูทดสอบขึ้นมาก่อน
    temp_food = {
        "name": "เมนูสำหรับทดสอบลบโดย Admin",
        "restaurant_id": 1,
        "price": 30,
        "kcal": 250,
        "protein": 10,
        "carbohydrate": 30,
        "fat": 5
    }
    status_create, created = client.post("/foods", data=temp_food)
    assert status_create == 201, "สร้างเมนูชั่วคราวสำเร็จ"
    food_id = created["id"]

    print(f"\n[Test 09] ลบเมนูอาหาร: DELETE /api/foods/{food_id}")

    # 2. แอดมินทำการลบเมนู
    status_del, res_del = client.delete(f"/foods/{food_id}")
    print(f"  Delete Response Status: {status_del}")
    print(f"  Delete Response Body: {res_del}")
    assert status_del == 200, f"คาดหวัง Status 200 แต่ได้ {status_del}"
    assert res_del.get("success") is True, "ต้องแจ้ง success: true"

    # 3. ตรวจสอบว่าเมนูนั้นถูกลบจริง ไม่สามารถค้นหาได้อีก
    status_check, _ = client.get(f"/foods/{food_id}")
    assert status_check == 404, "เมนูที่ถูกลบไปแล้วต้องไม่พบ (404)"

    print("  \033[92m✔ ผ่านการทดสอบ: ผู้ดูแลระบบสามารถลบเมนูอาหารออกจากฐานข้อมูลได้สมบูรณ์\033[0m")
    return True

if __name__ == "__main__":
    test_admin_delete_food()
