#!/usr/bin/env bash
# ======================================================
#   ชุดทดสอบระบบ University Food Kcal (Test Runner)
#   มหาวิทยาลัยราชภัฏนครปฐม (Nakhon Pathom Rajabhat University)
# ======================================================

set -e

echo "======================================================"
echo "  ชุดทดสอบระบบ University Food Kcal (Test Runner)"
echo "  มหาวิทยาลัยราชภัฏนครปฐม (Nakhon Pathom Rajabhat University)"
echo "======================================================"
echo ""
echo "กำลังเริ่มต้นการรัน Test..."
echo ""

echo "[1/2] เริ่มต้นการทดสอบ Node.js / Express API Tests..."
npm test

echo ""
echo "------------------------------------------------------"
echo "[2/2] เริ่มต้นการทดสอบ Python Function Test Suite (เเบ่งตามหัวข้อ)..."
if [ -f "test_cases_suite.py" ]; then
    python3 test_cases_suite.py || python test_cases_suite.py
elif [ -f "backend/run_tests.py" ]; then
    python3 backend/run_tests.py || python backend/run_tests.py
fi

echo ""
echo "======================================================"
echo "  🎉 เสร็จสิ้นการรันชุดทดสอบทั้งหมดเรียบร้อยแล้ว!"
echo "======================================================"
