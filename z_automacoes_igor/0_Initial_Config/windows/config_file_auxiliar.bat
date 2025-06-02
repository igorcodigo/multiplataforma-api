@REM Esse script automatiza o processo de criação das primeiras migrações, aplicação das migrações no banco de dados e criação de um superusuário para um projeto Django.
@REM Após a conclusão, ele remove o diretório de configurações iniciais do projeto.

@echo off


REM Muda para o diretório acima do diretorio atual
cd ..
@REM REM Armazena o diretório atual
@REM set CURRENT_DIR=%CD%

cd ..
cd ..
call .venv\Scripts\activate

echo Criando migracoes...
python manage.py makemigrations
if errorlevel 1 (
    echo Erro ao criar migracoes
    pause
    exit /b 1
)

echo Para realizar as migracoes no banco de dados pressione Enter 
pause >nul
python manage.py migrate

echo Criando super usuario
python manage.py createsuperuser

echo Para realizar as migracoes no banco de dados pressione Enter 
pause >nul

@REM REM Remove o diretório atual e seu conteúdo
@REM @REM cd ..
@REM rmdir /s /q "%CURRENT_DIR%"

pause'''''''''