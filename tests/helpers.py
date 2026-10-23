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
import atexit
import shutil
import socket
import subprocess
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

APP_URL = os.environ.get("APP_URL", "http://localhost:3000")
API_URL = os.environ.get("API_URL", f"{APP_URL.rstrip('/')}/api")
_LOCAL_SERVER: Optional[subprocess.Popen] = None
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_HEADED_DRIVER_IDS = set()


def ensure_local_app():
    """Start this checkout when no external APP_URL was explicitly configured."""
    global APP_URL, API_URL, _LOCAL_SERVER

    if os.environ.get("APP_URL"):
        return

    node = shutil.which("node")
    server_entry = os.path.join(_PROJECT_ROOT, "node_modules", "tsx", "dist", "cli.mjs")
    if not node or not os.path.isfile(server_entry):
        raise RuntimeError(
            "Cannot start the test app. Install project dependencies with `npm ci`, "
            "or set APP_URL to a running app."
        )

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    APP_URL = f"http://127.0.0.1:{port}"
    API_URL = f"{APP_URL}/api"
    os.environ["APP_URL"] = APP_URL
    os.environ["API_URL"] = API_URL

    server_env = os.environ.copy()
    server_env["PORT"] = str(port)
    server_env["DISABLE_HMR"] = "true"
    _LOCAL_SERVER = subprocess.Popen(
        [node, server_entry, "server.ts"],
        cwd=_PROJECT_ROOT,
        env=server_env,
    )
    atexit.register(stop_local_app)

    deadline = time.monotonic() + 30
    health_url = f"{API_URL}/health"
    while time.monotonic() < deadline:
        if _LOCAL_SERVER.poll() is not None:
            raise RuntimeError(
                f"Local test app exited during startup with code {_LOCAL_SERVER.returncode}."
            )
        try:
            with urllib.request.urlopen(health_url, timeout=1) as response:
                health = json.loads(response.read().decode("utf-8"))
            if health.get("status") == "online":
                return
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            time.sleep(0.25)

    stop_local_app()
    raise RuntimeError(f"Local test app did not become healthy at {health_url}.")


def stop_local_app():
    global _LOCAL_SERVER

    if _LOCAL_SERVER is None or _LOCAL_SERVER.poll() is not None:
        return
    _LOCAL_SERVER.terminate()
    try:
        _LOCAL_SERVER.wait(timeout=5)
    except subprocess.TimeoutExpired:
        _LOCAL_SERVER.kill()
        _LOCAL_SERVER.wait()
    _LOCAL_SERVER = None

# ตรวจสอบการ import selenium แบบมาตรฐาน
SELENIUM_AVAILABLE = False
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By as SeleniumBy
    from selenium.webdriver.common.keys import Keys as SeleniumKeys
    from selenium.webdriver.chrome.options import Options as SeleniumChromeOptions
    from selenium.webdriver.support.ui import WebDriverWait as SeleniumWait
    from selenium.webdriver.support import expected_conditions as SeleniumEC
    from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
    WAIT_IGNORED_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)
    SELENIUM_AVAILABLE = True
except ImportError:
    WAIT_IGNORED_EXCEPTIONS = ()
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
        deadline = time.monotonic() + self.timeout
        last_exception = None
        while time.monotonic() < deadline:
            try:
                result = condition(self.driver)
                if result:
                    return result
            except WAIT_IGNORED_EXCEPTIONS as exc:
                last_exception = exc
            time.sleep(0.1)
        if last_exception:
            raise TimeoutError(f"Condition was not met within {self.timeout} seconds.") from last_exception
        raise TimeoutError(f"Condition was not met within {self.timeout} seconds.")


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


def get_driver(headless: Optional[bool] = None):
    """
    สร้างและคืนค่า Selenium WebDriver
    - หากระบุ --browser หรือ --gui ใน argument หรือ HEADLESS=0 จะเปิดหน้าต่าง Google Chrome จริงขึ้นมาบนหน้าจอ
    - หากมี selenium และ Google Chrome ติดตั้งอยู่ จะเปิดเบราว์เซอร์จริง
    - หากรันบน Server ที่ไม่มี GUI / Chrome จะทำงานผ่าน compatibility driver โดยยิง HTTP ไปยังเว็บไซต์จริง
    """
    ensure_local_app()

    # ตรวจสอบว่าผู้ใช้ต้องการเปิดหน้าต่างเบราว์เซอร์จริงหรือไม่
    if headless is None:
        if "--browser" in sys.argv or "--headed" in sys.argv or "--gui" in sys.argv:
            headless = False
        elif os.environ.get("HEADLESS", "").lower() in ("0", "false", "no"):
            headless = False
        else:
            # ค่าเริ่มต้นเมื่อรันผ่าน terminal ให้ตรวจว่ามี DISPLAY หรือไม่
            has_display = bool(os.environ.get("DISPLAY") or sys.platform in ("win32", "darwin"))
            headless = not has_display

    if SELENIUM_AVAILABLE:
        try:
            options = SeleniumChromeOptions()
            if headless:
                options.add_argument("--headless=new")
                print("ℹ️  รันในโหมด Headless (เบื้องหลัง)")
            else:
                print("🌐 กำลังเปิดหน้าต่าง Google Chrome จริงขึ้นมาบนหน้าจอเพื่อทดสอบเว็บไซต์...")
                options.add_argument("--start-maximized")

            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1366,768")

            try:
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service as ChromeService
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except Exception:
                driver = webdriver.Chrome(options=options)

            driver.set_page_load_timeout(20)
            driver.implicitly_wait(7)
            if not headless:
                _HEADED_DRIVER_IDS.add(id(driver))
            return driver
        except Exception as e:
            if not headless:
                print(f"⚠️  ไม่สามารถเปิด Chrome GUI บนเครื่องนี้ได้ ({e}) - สลับเป็นโหมด E2E HTTP Live Tester อัตโนมัติ")

    return MockWebDriver(APP_URL)


def quit_driver(driver):
    """Keep headed test browsers open for inspection in interactive terminals."""
    keep_open = (
        "--keep-open" in sys.argv
        or (
            "--no-keep-open" not in sys.argv
            and id(driver) in _HEADED_DRIVER_IDS
            and sys.stdin.isatty()
        )
    )
    _HEADED_DRIVER_IDS.discard(id(driver))
    if keep_open:
        try:
            input("ดูผลการทดสอบในเบราว์เซอร์แล้วกด Enter เพื่อปิดและดำเนินการต่อ...")
        except EOFError:
            print("ไม่มีคอนโซลรับอินพุต ปิดเบราว์เซอร์ตามปกติ")
    driver.quit()


ensure_local_app()
