@echo off
echo Iniciando Backend Tesla Cotizador v3.0...
call venv\Scripts\activate
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
pause
