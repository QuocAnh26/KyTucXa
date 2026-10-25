@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 (
        echo Khong tao duoc moi truong Python. Hay kiem tra Python da duoc cai dat va co trong PATH chua.
        pause
        exit /b 1
    )
)

call ".venv\Scripts\activate.bat"

if exist "requirements.txt" (
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Cai thu vien that bai.
        pause
        exit /b 1
    )
)

python main.py
pause