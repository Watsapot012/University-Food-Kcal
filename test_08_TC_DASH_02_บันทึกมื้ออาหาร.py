#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Test Case ID : TC-DASH-02
หน้าจอ       : หน้าไดอารี่ประจำวัน (Daily Dashboard Page)
ฟังก์ชัน      : บันทึกมื้ออาหารลงไดอารี่ (Log Daily Meal Entry)
ข้อมูลนำเข้า  : บันทึก "ข้าวกะเพราไก่" (640 kcal) ลงในมื้อกลางวัน
ผลลัพธ์ที่คาดหวัง: แคลอรี่สะสมเพิ่มขึ้น 640 kcal และมีรายการอาหารใหม่ปรากฏในตาราง
================================================================================
"""

class DailyDashboardState:
    def __init__(self, target_calories: int = 2000):
        self.target = target_calories
        self.meals = [
            {"id": "m1", "name": "แซนด์วิชไข่ต้ม", "calories": 250, "type": "breakfast"}
        ]

    def add_meal(self, name: str, calories: int, meal_type: str):
        new_meal = {
            "id": f"m{len(self.meals) + 1}",
            "name": name,
            "calories": calories,
            "type": meal_type,
            "timestamp": "12:30 น."
        }
        self.meals.append(new_meal)
        return new_meal

    def get_total_calories(self):
        return sum(m["calories"] for m in self.meals)

    def get_remaining_calories(self):
        return self.target - self.get_total_calories()


def test_log_meal_entry():
    print("=" * 70)
    print("🧪 รันแบบทดสอบ: TC-DASH-02 (ไดอารี่ - บันทึกมื้ออาหารลงตาราง)")
    print("=" * 70)

    dashboard = DailyDashboardState(target_calories=2000)
    print(f"👉 1. สถานะเริ่มต้น: ทานไปแล้ว {dashboard.get_total_calories()} kcal / เป้าหมาย {dashboard.target} kcal")

    # 2. Input การบันทึกมื้ออาหารกลางวัน
    meal_name = "ข้าวกะเพราไก่ไข่ดาว"
    meal_kcal = 640
    meal_type = "lunch"
    print(f"👉 2. Input: บันทึก '{meal_name}' ({meal_kcal} kcal) ลงมื้อกลางวัน")

    # 3. ดำเนินการเพิ่มมื้ออาหาร
    new_entry = dashboard.add_meal(meal_name, meal_kcal, meal_type)

    total_used = dashboard.get_total_calories()
    remaining = dashboard.get_remaining_calories()

    print(f"👉 3. ผลลัพธ์หลังบันทึก:")
    print(f"   - รายการในตารางทั้งหมด : {len(dashboard.meals)} รายการ")
    print(f"   - แคลอรี่สะสมรวม      : {total_used} kcal (250 + 640)")
    print(f"   - แคลอรี่คงเหลือวันนี้ : {remaining} kcal (2000 - 890)")

    # 4. Assertions ตรวจสอบ
    assert len(dashboard.meals) == 2, "ต้องมี 2 รายการในตาราง"
    assert new_entry["name"] == "ข้าวกะเพราไก่ไข่ดาว"
    assert total_used == 890, f"แคลอรี่สะสมต้องเป็น 890 kcal แต่คำนวณได้ {total_used}"
    assert remaining == 1110, f"แคลอรี่คงเหลือต้องเป็น 1110 kcal แต่คำนวณได้ {remaining}"

    print("\n\033[92m✔ ผลการทดสอบ: ผ่าน (PASS) - บันทึกมื้ออาหารลงตารางและคำนวณแคลอรี่สะสมถูกต้องสมบูรณ์\033[0m\n")


if __name__ == "__main__":
    test_log_meal_entry()
