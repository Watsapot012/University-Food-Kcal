#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Test Runner สำหรับโฟลเดอร์ tests/
สามารถสั่งรัน: python tests/run_tests.py
"""

import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from test_portal_10_cases import run_all_cases

if __name__ == "__main__":
    sys.exit(run_all_cases())
