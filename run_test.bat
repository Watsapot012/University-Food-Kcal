@echo off
chcp 65001 > nul
cls
echo ======================================================
echo   ชุดทดสอบระบบ University Food Kcal (Test Runner)
echo   มหาวิทยาลัยราชภัฏนครปฐม (Nakhon Pathom Rajabhat University)
echo ======================================================
echo.
echo กำลังเริ่มต้นการรัน Test...
echo.

:: ตรวจสอบการรัน Node / TypeScript Tests
echo [1/2] เริ่มต้นการทดสอบ Node.js / Express API Tests...
call npm test
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Node.js Tests ไม่ผ่าน! กรุณาตรวจสอบข้อผิดพลาดด้านบน
    goto python_test
) else (
    echo.
    echo ✅ Node.js Tests ผ่านทั้งหมด!
)

:python_test
echo.
echo ------------------------------------------------------
echo [2/2] เริ่มต้นการทดสอบ Python Function Test Suite (เเบ่งตามหัวข้อ)...
if exist test_cases_suite.py (
    python test_cases_suite.py
) else if exist backend\run_tests.py (
    python backend\run_tests.py
) else (
    echo ไม่พบไฟล์ทดสอบสำหรับ Python
)

echo.
echo ======================================================
echo   เสร็จสิ้นการรันชุดทดสอบทั้งหมด
echo ======================================================
pause
