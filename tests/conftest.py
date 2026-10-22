# -*- coding: utf-8 -*-
"""
Pytest Fixtures configuration for University Food Kcal test suite
"""

import os
import sys
import pytest

# เพิ่ม directory เข้า sys.path
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import ApiClient, load_state, save_state

@pytest.fixture(scope="session")
def client():
    """Fixture สำหรับ ApiClient"""
    return ApiClient()

@pytest.fixture(scope="session")
def test_state():
    """Fixture สำหรับโหลดข้อมูล State"""
    return load_state()
