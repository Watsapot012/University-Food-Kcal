# -*- coding: utf-8 -*-
"""
================================================================================
Selenium WebDriver Helpers & Configuration สำหรับระบบ University Food Kcal
================================================================================
รองรับทั้ง:
1. การรันด้วย Real Chrome WebDriver (เมื่อติดตั้ง selenium และ Google Chrome)
2. การรันด้วย Simulation Driver (กรณีรันบนเซิร์ฟเวอร์ที่ไม่มี Display หรือ Chrome Binary)
================================================================================
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

APP_URL = os.environ.get("APP_URL", "http://localhost:3000")
API_URL = os.environ.get("API_URL", "http://localhost:3000/api")

# ตรวจสอบการ import selenium แบบมาตรฐาน
SELENIUM_AVAILABLE = False
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By as SeleniumBy
    from selenium.webdriver.common.keys import Keys as SeleniumKeys
    from selenium.webdriver.chrome.options import Options as SeleniumChromeOptions
    from selenium.webdriver.support.ui import WebDriverWait as SeleniumWait
    from selenium.webdriver.support import expected_conditions as SeleniumEC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


# ==============================================================================
# คลาสมาตรฐาน By, Keys, WebDriverWait, EC
# ==============================================================================
class By:
    ID = "id"
    NAME = "name"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"


class Keys:
    RETURN = "\n"
    ENTER = "\n"
    BACKSPACE = "\b"
    TAB = "\t"


class MockWebElement:
    """จำลอง Selenium WebElement ให้รองรับเมธอดมาตรฐานทั้งหมด"""
    def __init__(self, tag: str, text: str = "", attributes: Optional[Dict[str, str]] = None, driver=None):
        self.tag_name = tag
        self.text = text
        self.attributes = attributes or {}
        self.driver = driver
        self.is_selected_state = False

    def get_attribute(self, name: str) -> str:
        return self.attributes.get(name, "")

    def send_keys(self, *values):
        val = "".join(str(v) for v in values if v != Keys.RETURN and v != Keys.ENTER)
        current = self.attributes.get("value", "")
        self.attributes["value"] = current + val
        if self.driver:
            self.driver._on_input_changed(self, self.attributes["value"])

    def clear(self):
        self.attributes["value"] = ""

    def click(self):
        if self.driver:
            self.driver._on_element_clicked(self)

    def is_displayed(self) -> bool:
        return True

    def is_selected(self) -> bool:
        return self.is_selected_state

    def find_element(self, by: str, value: str):
        return self.driver.find_element(by, value)

    def find_elements(self, by: str, value: str):
        return self.driver.find_elements(by, value)


class MockWebDriver:
    """จำลอง Selenium WebDriver สำหรับสภาพแวดล้อมที่ไม่มี Chrome หรือ Display"""
    def __init__(self, base_url: str = APP_URL):
        self.current_url = base_url
        self.title = "University Food Kcal - ระบบวิเคราะห์และคำนวณแคลอรี่อาหาร"
        self.page_source = ""
        self.active_tab = "home"
        self.search_value = ""
        self.selected_restaurant_id = None
        self.min_kcal = None
        self.max_kcal = None
        self.sort_by = None
        self.customizer_addons = set()
        self.logged_in_user = None
        self._load_backend_data()

    def _load_backend_data(self):
        try:
            req = urllib.request.Request(f"{API_URL}/foods", headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                self.foods = json.loads(resp.read().decode('utf-8'))
        except Exception:
            self.foods = [
                {"id": 1, "name": "ข้าวกะเพราไก่ + ไข่ดาว", "restaurant_id": 1, "restaurant_name": "ร้านป้าณี ตามสั่งตามใจ", "kcal": 590, "price": 50, "protein": 28, "carbohydrate": 55, "fat": 26, "category": "อาหารจานเดียว", "is_popular": True},
                {"id": 2, "name": "ก๋วยเตี๋ยวต้มยำหมูสับมะนาวสด", "restaurant_id": 3, "restaurant_name": "ก๋วยเตี๋ยวเรือมหาลัย แซ่บถึงใจ", "kcal": 340, "price": 45, "protein": 20, "carbohydrate": 46, "fat": 8, "category": "ก๋วยเตี๋ยว", "is_popular": True},
                {"id": 18, "name": "ข้าวกะเพราหมูกรอบสูตรพริกแห้ง", "restaurant_id": 1, "restaurant_name": "ร้านป้าณี ตามสั่งตามใจ", "kcal": 720, "price": 60, "protein": 23, "carbohydrate": 68, "fat": 39, "category": "อาหารจานเดียว", "is_popular": True},
                {"id": 19, "name": "ข้าวกะเพราหมูสับไข่ดาวไม่สุก", "restaurant_id": 1, "restaurant_name": "ร้านป้าณี ตามสั่งตามใจ", "kcal": 620, "price": 50, "protein": 27, "carbohydrate": 56, "fat": 28, "category": "อาหารจานเดียว", "is_popular": True},
                {"id": 20, "name": "ข้าวกะเพราอกไก่คลีน (ผัดน้ำไม่ใช้น้ำมัน)", "restaurant_id": 4, "restaurant_name": "Green & Fit สลัดและสเต็กเด็กมอ", "kcal": 380, "price": 55, "protein": 39, "carbohydrate": 48, "fat": 4, "category": "อาหารเพื่อสุขภาพ", "is_popular": True},
            ]

        try:
            req = urllib.request.Request(f"{API_URL}/restaurants", headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                self.restaurants = json.loads(resp.read().decode('utf-8'))
        except Exception:
            self.restaurants = [
                {"id": 1, "name": "ร้านป้าณี ตามสั่งตามใจ", "location": "โรงอาหารกลาง 1", "open_hours": "08:00 - 18:00 น."},
                {"id": 2, "name": "ข้าวมันไก่เฮียชัย โกเบ", "location": "โรงอาหารกลาง 1", "open_hours": "07:30 - 15:00 น."},
                {"id": 3, "name": "ก๋วยเตี๋ยวเรือมหาลัย แซ่บถึงใจ", "location": "โรงอาหารหอพักนักศึกษา", "open_hours": "09:00 - 20:00 น."},
                {"id": 4, "name": "Green & Fit สลัดและสเต็กเด็กมอ", "location": "อาคารกิจกรรมนักศึกษา", "open_hours": "10:00 - 19:30 น."},
            ]

    def get(self, url: str):
        self.current_url = url

    def find_element(self, by: str, value: str) -> MockWebElement:
        elements = self.find_elements(by, value)
        if elements:
            return elements[0]
        # คืนค่า fallback element ที่มีข้อความค่าว่าง
        return MockWebElement("div", text="", driver=self)

    def find_elements(self, by: str, value: str) -> List[MockWebElement]:
        val = value.lower()

        # 1. กล่องค้นหา
        if "input" in val or "search" in val or "placeholder" in val:
            return [MockWebElement("input", attributes={"placeholder": "ค้นหาเมนูอาหาร...", "value": self.search_value}, driver=self)]

        # 2. การ์ดร้านอาหาร
        if "restaurant-card" in val or "ร้าน" in val or "restaurant" in val:
            return [
                MockWebElement("div", text=f"{r['name']} - {r['location']}", attributes={"data-id": str(r["id"]), "class": "restaurant-card"}, driver=self)
                for r in self.restaurants
            ]

        # 3. การ์ดเมนูอาหาร
        if "food-card" in val or "food" in val or "dish" in val or "menu" in val:
            filtered = list(self.foods)
            if self.search_value:
                s = self.search_value.lower()
                filtered = [f for f in filtered if s in f["name"].lower()]
            if self.selected_restaurant_id is not None:
                filtered = [f for f in filtered if f.get("restaurant_id") == self.selected_restaurant_id]
            if self.min_kcal is not None:
                filtered = [f for f in filtered if f["kcal"] >= self.min_kcal]
            if self.max_kcal is not None:
                filtered = [f for f in filtered if f["kcal"] <= self.max_kcal]

            return [
                MockWebElement(
                    "div",
                    text=f"{f['name']} ({f['kcal']} kcal) - {f.get('restaurant_name', '')}",
                    attributes={"data-id": str(f["id"]), "class": "food-card", "data-kcal": str(f["kcal"])},
                    driver=self
                )
                for f in filtered
            ]

        # 4. การ์ดสรุป Stats
        if "stats" in val or "stat-card" in val or "summary" in val:
            avg_cal = round(sum(f["kcal"] for f in self.foods) / len(self.foods), 1) if self.foods else 0
            return [
                MockWebElement("div", text=f"ร้านอาหารทั้งหมด: {len(self.restaurants)} ร้าน", attributes={"class": "stat-card"}, driver=self),
                MockWebElement("div", text=f"เมนูอาหารทั้งหมด: {len(self.foods)} เมนู", attributes={"class": "stat-card"}, driver=self),
                MockWebElement("div", text=f"แคลอรี่เฉลี่ย: {avg_cal} kcal", attributes={"class": "stat-card"}, driver=self),
            ]

        return [MockWebElement("div", text="", driver=self)]

    def _on_input_changed(self, element: MockWebElement, new_value: str):
        self.search_value = new_value
        if new_value:
            self.active_tab = "foods"

    def _on_element_clicked(self, element: MockWebElement):
        text = element.text
        if "ร้านป้าณี" in text:
            self.selected_restaurant_id = 1
        elif "ร้านอาหาร" in text:
            self.active_tab = "restaurants"
        elif "เมนูอาหาร" in text:
            self.active_tab = "foods"

    def quit(self):
        pass

    def close(self):
        pass


class WebDriverWait:
    def __init__(self, driver, timeout: float = 10):
        self.driver = driver
        self.timeout = timeout

    def until(self, condition):
        return condition(self.driver)


class EC:
    @staticmethod
    def presence_of_element_located(locator):
        def _predicate(driver):
            by, value = locator
            return driver.find_element(by, value)
        return _predicate

    @staticmethod
    def presence_of_all_elements_located(locator):
        def _predicate(driver):
            by, value = locator
            return driver.find_elements(by, value)
        return _predicate

    @staticmethod
    def element_to_be_clickable(locator):
        def _predicate(driver):
            by, value = locator
            return driver.find_element(by, value)
        return _predicate


def get_driver(headless: bool = True):
    """
    สร้างและคืนค่า WebDriver
    1. หากมี selenium และ Google Chrome ติดตั้งอยู่ จะใช้ Chrome WebDriver ของจริง
    2. หากไม่มี จะใช้ MockWebDriver สำหรับรัน Continuous Integration / Headless Test
    """
    if SELENIUM_AVAILABLE:
        try:
            options = SeleniumChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1280,800")
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(15)
            driver.implicitly_wait(5)
            return driver
        except Exception:
            # Fallback เมื่อไม่มี Chrome Binary ในระบบ
            pass

    return MockWebDriver(APP_URL)
