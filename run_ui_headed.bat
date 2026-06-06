@echo off
echo ============================================
echo  Running SauceDemo UI tests WITH browser visible
echo  (you should see Chrome open and run tests)
echo ============================================
call .venv\Scripts\activate.bat
pytest assignment1-ui --headed -v
echo.
echo Done. Press any key to close...
pause >nul
