@echo off
chcp 65001 > nul
echo ========================================================
echo   Executive Investment Assistant - Live Price Updater
echo ========================================================
echo.
python update_prices.py
echo.
echo ========================================================
echo  อัปเดตข้อมูลเสร็จสิ้น! คุณสามารถเปิดหรือรีเฟรช portfolio_tracker.html ได้ทันที
echo ========================================================
pause
