#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test 07: ทดสอบการลบข้อมูล (User Delete: ลบรายการอาหารที่บันทึกไว้)
ฟังก์ชัน: DELETE /api/logs/:id
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import ApiClient, load_state

def test_delete_user_log():
    """ทดสอบการลบรายการอาหารที่บันทึกไว้ในบันทึกประจำวัน"""
    client = ApiClient()
    state = load_state()
    user_id = state.get("userId", 1)
    target_log_id = state.get("lastCreatedLogId")

    # หากไม่มี log id จาก Test 02 ให้สร้างขึ้นมาชั่วคราวเพื่อลบ
    if not target_log_id:
        _, temp = client.post("/logs", data={
            "userId": user_id,
            "name": "รายการทดสอบสำหรับลบ",
            "calories": 200
        })
        target_log_id = temp.get("id", "log-1")

    status, response = client.delete(f"/logs/{target_log_id}?userId={user_id}")
    print(f"\n[Test 07] DELETE /api/logs/{target_log_id}?userId={user_id}")
    print(f"  Response Status: {status}")
    print(f"  Response Body: {response}")

    assert status == 200, f"คาดหวัง Status 200 แต่ได้ {status}"
    assert response.get("success") is True, "ผลลัพธ์การลบต้องเป็น success: true"

    # ตรวจสอบซ้ำว่ารายการนั้นไม่มีอยู่แล้ว
    _, current_logs = client.get(f"/logs?userId={user_id}")
    remaining_ids = [m.get("id") for m in current_logs.get("meals", [])]
    assert target_log_id not in remaining_ids, "รายการอาหารที่ถูกลบต้องไม่อยู่ในระบบแล้ว"

    print("  \033[92m✔ ผ่านการทดสอบ: ลบรายการข้อมูลที่ต้องการได้อย่างถูกต้อง\033[0m")
    return True

if __name__ == "__main__":
    test_delete_user_log()
