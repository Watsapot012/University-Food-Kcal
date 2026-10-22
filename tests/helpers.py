# -*- coding: utf-8 -*-
"""
Helpers and Test Utilities สำหรับระบบ University Food Kcal
ใช้มาตรฐาน Python Standard Library (urllib, json) ทำงานได้ทันทีทุกเครื่อง
"""

import os
import sys
import json
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, Any, Optional, Tuple

BASE_URL = os.environ.get("TEST_API_URL", "http://127.0.0.1:3000/api")
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".test_state.json")

def load_state() -> Dict[str, Any]:
    """โหลด State ที่บันทึกไว้ระหว่าง Test Cases"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_state(updates: Dict[str, Any]) -> None:
    """บันทึก State ลงใน .test_state.json"""
    state = load_state()
    state.update(updates)
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Could not save test state: {e}")

class ApiClient:
    """HTTP Client สำหรับส่ง Request ไปยัง API ของแอปพลิเคชัน"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/")

    def request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Tuple[int, Any]:
        """
        ส่ง HTTP request และคืนค่า (status_code, response_body_as_json_or_text)
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        req_headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
        }
        if headers:
            req_headers.update(headers)

        payload_bytes = None
        if data is not None:
            payload_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload_bytes,
            headers=req_headers,
            method=method.upper()
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.status
                body_raw = response.read().decode("utf-8")
                try:
                    body = json.loads(body_raw)
                except Exception:
                    body = body_raw
                return status, body
        except urllib.error.HTTPError as e:
            status = e.code
            body_raw = e.read().decode("utf-8")
            try:
                body = json.loads(body_raw)
            except Exception:
                body = body_raw
            return status, body
        except Exception as e:
            return 500, {"error": str(e)}

    def get(self, path: str, headers: Optional[Dict[str, str]] = None) -> Tuple[int, Any]:
        return self.request("GET", path, headers=headers)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Tuple[int, Any]:
        return self.request("POST", path, data=data, headers=headers)

    def put(self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Tuple[int, Any]:
        return self.request("PUT", path, data=data, headers=headers)

    def delete(self, path: str, headers: Optional[Dict[str, str]] = None) -> Tuple[int, Any]:
        return self.request("DELETE", path, headers=headers)

# ตรวจสอบตัวอักษรภาษาไทยว่าไม่เป็นภาษาต่างดาว (Mojibake)
def is_thai_clean(text: str) -> bool:
    if not text:
        return True
    mojibake = ["à¸", "à¹", "Ã", "Â", "เธ‚", "เน‰", "เธ"]
    return not any(m in text for m in mojibake)
