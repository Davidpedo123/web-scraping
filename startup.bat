@echo off
REM Activar entorno virtual si existe (opcional)
REM call env\Scripts\activate

echo Checking virtual environment...

if not exist ".\dependencies\Scripts\activate.bat" (
    echo Virtual environment "dependencies" not found. Creating...
    python -m venv dependencies
) else (
    echo Virtual environment "dependencies" already exists.
)

echo Activating virtual environment...
call .\dependencies\Scripts\activate.bat

echo Installing dependencies from requirements.txt...
pip install -r ".\src\app\lib\requirements.txt"

echo Running the project...
python ".\src\app\main.py"

pause
