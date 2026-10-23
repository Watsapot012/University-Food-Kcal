# -*- coding: utf-8 -*-
"""
Pytest Fixtures configuration for University Food Kcal Selenium test suite
"""

import os
import sys
import pytest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from helpers import get_driver, APP_URL, By, Keys, WebDriverWait, EC

@pytest.fixture(scope="function")
def driver():
    """Selenium WebDriver Fixture สำหรับแต่ละ Test Case"""
    drv = get_driver(headless=True)
    yield drv
    try:
        drv.quit()
    except Exception:
        pass
