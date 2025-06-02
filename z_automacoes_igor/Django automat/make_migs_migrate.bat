@REM @echo off
:: Move para o diretórioum nível acima
cd ..
:: Move para o diretórioum nível acima
cd ..

call .venv\Scripts\activate

echo Criando migracoes...
python manage.py makemigrations

echo Para realizar as migracoes no banco de dados pressione Enter 
pause >nul
python manage.py migrate

echo Pressione Enter para iniciar o servidor e abrir o Chrome no url desejado.
pause >nul

echo Iniciando o servidor e abrindo o Chrome...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" http://127.0.0.1:8001/admin/
python manage.py runserver 8001