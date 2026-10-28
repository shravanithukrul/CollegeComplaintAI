@echo off
title CollegeCare AI - Local Development Server
echo ============================================================
echo   CollegeCare AI - Starting Institutional Governance Server
echo ============================================================
echo.
echo Application will be live at: http://127.0.0.1:5000
echo Default Admin: username 'admin', password 'admin123'
echo Default Student: username 'student', password 'student123'
echo.
python app.py
pause
