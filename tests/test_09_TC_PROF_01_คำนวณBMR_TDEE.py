#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Test Case ID : TC-PROF-01
หน้าจอ       : หน้าโปรไฟล์และสุขภาพ (Profile Page)
ฟังก์ชัน      : คำนวณค่า BMR และ TDEE อัตโนมัติ (Mifflin-St Jeor Formula)
ข้อมูลนำเข้า  : เพศชาย, น้ำหนัก 65 กก., ส่วนสูง 175 ซม., อายุ 21 ปี, กิจกรรม 1.55 (ปานกลาง)
ผลลัพธ์ที่คาดหวัง: BMR คำนวณได้ 1,644 kcal และ TDEE คำนวณได้ 2,548 kcal
================================================================================
"""

def calculate_mifflin_bmr(weight: float, height: float, age: int, gender: str) -> int:
    """
    สูตร Mifflin-St Jeor
    - เพศชาย  : (10 * weight) + (6.25 * height) - (5 * age) + 5
    - เพศหญิง : (10 * weight) + (6.25 * height) - (5 * age) - 161
    """
    if gender == 'male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    return round(bmr)


def calculate_tdee_calories(bmr: int, activity_level: float) -> int:
    """
    สูตรคำนวณ TDEE = BMR * ระดับกิจกรรม
    """
    return round(bmr * activity_level)


def test_bmr_and_tdee_calculation():
    print("=" * 70)
    print("🧪 รันแบบทดสอบ: TC-PROF-01 (โปรไฟล์ - คำนวณ BMR และ TDEE อัตโนมัติ)")
    print("=" * 70)

    # 1. ข้อมูลนำเข้าของผู้ใช้
    weight = 65.0      # กิโลกรัม
    height = 175.0     # เซนติเมตร
    age = 21           # ปี
    gender = 'male'    # ชาย
    activity = 1.55    # ออกกำลังกายปานกลาง 3-5 วัน/สัปดาห์

    print(f"👉 1. Input ข้อมูลร่างกาย: เพศ={gender}, นน.={weight} กก., สส.={height} ซม., อายุ={age} ปี, กิจกรรม={activity}")

    # 2. Logic การคำนวณ
    # BMR  = 10(65) + 6.25(175) - 5(21) + 5
    #      = 650 + 1093.75 - 105 + 5 = 1643.75 -> 1644 kcal
    calculated_bmr = calculate_mifflin_bmr(weight, height, age, gender)

    # TDEE = 1644 * 1.55 = 2548.2 -> 2548 kcal
    calculated_tdee = calculate_tdee_calories(calculated_bmr, activity)

    print(f"👉 2. ผลการคำนวณทางวิทยาศาสตร์สุขภาพ:")
    print(f"   - พลังงานพื้นฐาน (BMR)  : {calculated_bmr} kcal/วัน")
    print(f"   - พลังงานรวมที่ใช้ (TDEE): {calculated_tdee} kcal/วัน")

    # 3. Assertions ตรวจสอบ
    assert calculated_bmr == 1644, f"BMR ต้องได้ 1644 kcal แต่คำนวณได้ {calculated_bmr}"
    assert calculated_tdee == 2548, f"TDEE ต้องได้ 2548 kcal แต่คำนวณได้ {calculated_tdee}"

    print("\n\033[92m✔ ผลการทดสอบ: ผ่าน (PASS) - สูตรคำนวณ BMR และ TDEE ให้ผลลัพธ์แม่นยำ 100%\033[0m\n")


if __name__ == "__main__":
    test_bmr_and_tdee_calculation()
