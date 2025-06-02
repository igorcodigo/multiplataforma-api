@echo off
echo Starting SQLite Database Backup...

REM Muda para o diretório principal do projeto
cd /d %~dp0\..

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Using system Python.
)

echo Pressione qualquer tecla para fazer o backup e enviar o arquivo do backup para o e-mail
pause 

REM Run the Django management command for backup
python manage.py backup_db

REM Deactivate virtual environment
if exist ".venv\Scripts\deactivate.bat" (
    call .venv\Scripts\deactivate.bat
)

echo Backup process completed.
pause