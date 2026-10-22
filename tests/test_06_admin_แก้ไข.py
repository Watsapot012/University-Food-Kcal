#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 06: ทดสอบผู้ดูแลระบบ (Admin) แก้ไขข้อมูลอาหารและสารอาหาร
ฟังก์ชัน: PUT /api/foods/:id
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import ApiClient

def test_admin_edit_food():
    """ทดสอบแอดมินแก้ไขข้อมูลราคาและแคลอรี่ของเมนูอาหาร"""
    client = ApiClient()

    # ดึงเมนูที่มีอยู่เพื่อนำ ID มาทดสอบแก้ไข
    status_get, foods = client.get("/foods")
    assert status_get == 200 and len(foods) > 0, "ต้องมีเมนูในระบบอย่างน้อย 1 รายการ"

    target_food = foods[0]
    target_id = target_food["id"]
    original_price = target_food.get("price", 50)

    # ส่งคำสั่งแก้ไขราคาและแคลอรี่
    update_payload = {
        "price": original_price + 5,
        "kcal": target_food.get("kcal", 500) + 10,
        "description": "ปรับปรุงสูตรอาหารใหม่เพื่อสุขภาพ นครปฐม"
    }

    status, response = client.put(f"/foods/{target_id}", data=update_payload)
    print(f"\n[Test 06] PUT /api/foods/{target_id} (Admin แก้ไขข้อมูลอาหาร)")
    print(f"  Update Payload: {update_payload}")
    print(f"  Response Status: {status}")
    print(f"  Updated Food: {response.get('name')}, Price: {response.get('price')}, Kcal: {response.get('kcal')}")

    assert status == 200, f"คาดหวัง Status 200 แต่ได้ {status}"
    assert response["price"] == update_payload["price"], "ราคาอาหารต้องถูกอัปเดต"
    assert response["kcal"] == update_payload["kcal"], "แคลอรี่ต้องถูกอัปเดต"

    print("  \033[92m✔ ผ่านการทดสอบ: ผู้ดูแลระบบสามารถแก้ไขข้อมูลอาหารได้สำเร็จ\033[0m")
    return True

if __name__ == "__main__":
    test_admin_edit_food()
