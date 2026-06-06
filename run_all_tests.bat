@echo off
echo ============================================
echo  Running ALL tests (UI + API)
echo  Browser runs in background (headless)
echo  HTML report will open when finished
echo ============================================
call .venv\Scripts\activate.bat
pytest -v
echo.
echo Opening HTML report in your browser...
start report.html
echo Done. Press any key to close...
pause >nul
