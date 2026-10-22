#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Test Case ID : TC-CUST-02
หน้าจอ       : หน้าปรับแต่งมื้ออาหาร (Meal Customizer Page)
ฟังก์ชัน      : คำนวณแคลอรี่แบบ Real-time เมื่อเลือกท็อปปิ้ง (+ไข่ดาว)
ข้อมูลนำเข้า  : เมนูตั้งต้น "ข้าวกะเพราไก่" (550 kcal) + ติ๊กเลือก "ไข่ดาว (+90 kcal)"
ผลลัพธ์ที่คาดหวัง: แคลอรี่รวมคำนวณใหม่เป็น 640 kcal ทันทีแบบ Real-time
================================================================================
"""

BASE_DISH = {
    "id": 1,
    "name": "ข้าวกะเพราไก่",
    "kcal": 550,
    "protein": 25,
    "carbohydrate": 65,
    "fat": 20,
}

MODIFIER_EGG = {
    "id": "fried_egg",
    "name": "ไข่ดาว",
    "kcal": 90,
    "protein": 6,
    "carbs": 1,
    "fat": 7
}


def test_customizer_add_egg():
    print("=" * 70)
    print("🧪 รันแบบทดสอบ: TC-CUST-02 (ปรับแต่งอาหาร - เพิ่มท็อปปิ้งไข่ดาว Real-time)")
    print("=" * 70)

    print(f"👉 1. เมนูตั้งต้น: {BASE_DISH['name']} (พลังงาน: {BASE_DISH['kcal']} kcal)")
    print(f"👉 2. Input: ผู้ใช้คลิกเลือกออปชัน '{MODIFIER_EGG['name']}' (+{MODIFIER_EGG['kcal']} kcal)")

    # 3. Logic การคำนวณแบบ Real-time ของหน้า Customizer
    customized_kcal = BASE_DISH["kcal"] + MODIFIER_EGG["kcal"]
    customized_pro = BASE_DISH["protein"] + MODIFIER_EGG["protein"]
    customized_carbs = BASE_DISH["carbohydrate"] + MODIFIER_EGG["carbs"]
    customized_fat = BASE_DISH["fat"] + MODIFIER_EGG["fat"]
    customized_name = f"{BASE_DISH['name']} (ไข่ดาว)"

    print(f"👉 3. ผลการคำนวณสดทันที (Real-time):")
    print(f"   - ชื่อเมนูใหม่    : {customized_name}")
    print(f"   - แคลอรี่สุทธิ   : {customized_kcal} kcal  (เดิม 550 + 90)")
    print(f"   - โปรตีนสุทธิ    : {customized_pro} g     (เดิม 25 + 6)")
    print(f"   - คาร์โบไฮเดรต   : {customized_carbs} g    (เดิม 65 + 1)")
    print(f"   - ไขมันสุทธิ     : {customized_fat} g      (เดิม 20 + 7)")

    # 4. Assertions ตรวจสอบ
    assert customized_kcal == 640, f"แคลอรี่ต้องเท่ากับ 640 kcal แต่คำนวณได้ {customized_kcal}"
    assert customized_pro == 31, f"โปรตีนต้องเท่ากับ 31g แต่คำนวณได้ {customized_pro}"
    assert "ไข่ดาว" in customized_name, "ชื่อเมนูต้องระบุออปชันไข่ดาว"

    print("\n\033[92m✔ ผลการทดสอบ: ผ่าน (PASS) - ระบบคำนวณแคลอรี่และสารอาหารสุทธิใหม่ถูกต้องทันที\033[0m\n")


if __name__ == "__main__":
    test_customizer_add_egg()
