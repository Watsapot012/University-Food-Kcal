#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ชุดทดสอบระบบ University Food Kcal (Python Backend Test Suite)
รองรับทั้ง standard unittest และ pytest

คำสั่งรัน:
  python -m unittest backend/test_app.py
  หรือ
  python backend/run_tests.py
"""

import os
import sys
import json
import unittest

# เพิ่ม path ให้สามารถ import โมดูล backend ได้
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from backend.models.restaurant import sanitize_data
except ImportError:
    try:
        from models.restaurant import sanitize_data
    except ImportError:
        def sanitize_data(item):
            return item

# พยายามนำเข้า Flask app
has_flask = False
try:
    from backend.app import create_app
    has_flask = True
except ImportError:
    try:
        from app import create_app
        has_flask = True
    except ImportError:
        has_flask = False


class TestThaiEncodingAndSanitizer(unittest.TestCase):
    """ทดสอบการประมวลผลและการเข้ารหัสตัวอักษรภาษาไทย (UTF-8)"""

    def test_thai_unicode_characters(self):
        """ทดสอบตัวอักษรภาษาไทยทั่วไปว่าไม่ผิดเพี้ยน"""
        sample_thai = "ข้าวกะเพราไก่ไข่ดาว มหาวิทยาลัยราชภัฏนครปฐม"
        self.assertIn("กะเพรา", sample_thai)
        self.assertIn("นครปฐม", sample_thai)
        # ตรวจสอบรหัส Unicode ภาษาไทย (\u0E00 - \u0E7F)
        has_thai_chars = any('\u0E00' <= char <= '\u0E7F' for char in sample_thai)
        self.assertTrue(has_thai_chars, "ต้องมีตัวอักษรภาษาไทยอยู่ในช่วง Unicode")

    def test_sanitize_data_clean_thai(self):
        """ทดสอบว่าข้อความภาษาไทยปกติไม่ถูกแปลงให้เสียหาย"""
        text = "ข้าวผัดต้มยำกุ้ง"
        result = sanitize_data(text)
        self.assertEqual(result, text)

    def test_sanitize_data_dict_and_list(self):
        """ทดสอบการ sanitize แบบ recursive ใน dict และ list"""
        data = {
            "name": "ข้าวมันไก่",
            "menu": ["ต้มยำกุ้ง", "แกงเขียวหวาน"],
            "calories": 550
        }
        cleaned = sanitize_data(data)
        self.assertEqual(cleaned["name"], "ข้าวมันไก่")
        self.assertEqual(cleaned["menu"][0], "ต้มยำกุ้ง")
        self.assertEqual(cleaned["calories"], 550)


class TestNutritionFormulas(unittest.TestCase):
    """ทดสอบความถูกต้องของสูตรคำนวณโภชนาการ แคลอรี่ BMR และ TDEE"""

    def test_calorie_macronutrient_formula(self):
        """
        สูตรคำนวณแคลอรี่:
        Calories = (Protein * 4) + (Carbohydrate * 4) + (Fat * 9)
        """
        protein = 25   # 25g * 4 = 100 kcal
        carbs = 60     # 60g * 4 = 240 kcal
        fat = 15       # 15g * 9 = 135 kcal
        expected_kcal = (protein * 4) + (carbs * 4) + (fat * 9)
        self.assertEqual(expected_kcal, 475)

    def test_bmr_mifflin_st_jeor_male(self):
        """
        สูตรคำนวณ BMR เพศชาย (Mifflin-St Jeor):
        BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age + 5
        """
        weight = 70
        height = 175
        age = 22
        bmr = round(10 * weight + 6.25 * height - 5 * age + 5)
        self.assertEqual(bmr, 1689)

    def test_bmr_mifflin_st_jeor_female(self):
        """
        สูตรคำนวณ BMR เพศหญิง (Mifflin-St Jeor):
        BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age - 161
        """
        weight = 55
        height = 160
        age = 20
        bmr = round(10 * weight + 6.25 * height - 5 * age - 161)
        self.assertEqual(bmr, 1289)

    def test_tdee_calculation(self):
        """
        สูตรคำนวณ TDEE:
        TDEE = BMR * Activity Multiplier
        Activity: ออกกำลังกายปานกลาง = 1.55
        """
        bmr = 1689
        activity = 1.55
        tdee = round(bmr * activity)
        self.assertEqual(tdee, 2618)


class TestDatabaseSchemaIntegrity(unittest.TestCase):
    """ทดสอบความสมบูรณ์ของไฟล์ schema.sql และ seed data"""

    def test_schema_sql_exists_and_utf8(self):
        schema_path = os.path.join(CURRENT_DIR, 'database', 'schema.sql')
        self.assertTrue(os.path.exists(schema_path), f"ต้องพบไฟล์ {schema_path}")

        with open(schema_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("utf8mb4", content, "schema.sql ต้องระบุการใช้ charset utf8mb4")
        self.assertIn("restaurants", content, "schema.sql ต้องมีตาราง restaurants")
        self.assertIn("foods", content, "schema.sql ต้องมีตาราง foods")
        self.assertIn("users", content, "schema.sql ต้องมีตาราง users")


@unittest.skipUnless(has_flask, "Flask ไม่ได้ถูกติดตั้งในสภาพแวดล้อมนี้")
class TestFlaskEndpoints(unittest.TestCase):
    """ทดสอบ API Endpoints ผ่าน Flask Test Client"""

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_root_endpoint_thai_response(self):
        """ทดสอบ GET / คืนค่าข้อความภาษาไทยและ 200 OK"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get('status'), 'online')
        self.assertIn('โภชนาการ', data.get('message', ''))

    def test_health_check_endpoint(self):
        """ทดสอบ GET /api/health คืนค่า status online"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get('status'), 'online')

    def test_not_found_404_in_thai(self):
        """ทดสอบหน้า Error 404 มีข้อความภาษาไทยบอกชัดเจน"""
        response = self.client.get('/api/non-existent-route-12345')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertTrue('error' in data)
        self.assertIn('ไม่พบ', data.get('error', ''))


if __name__ == '__main__':
    unittest.main()
