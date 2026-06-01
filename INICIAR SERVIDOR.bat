@echo off
title PharmaTech IA - Servidor
color 0A
echo.
echo  ==================================================
echo    PharmaTech NeuroScience - Iniciando Servidor...
echo  ==================================================
echo.
echo  Abre tu navegador en: http://127.0.0.1:5000
echo.
echo  Para cerrar el servidor presiona CTRL+C
echo.
cd /d "%~dp0"
.venv\Scripts\python app.py
pause
