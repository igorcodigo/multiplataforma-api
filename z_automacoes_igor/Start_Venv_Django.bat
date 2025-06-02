cd ..
:: Move para o diretório principal (um nível acima da subpasta "utilitários")

call .venv\Scripts\activate

:: Apenas lista as bibliotecas que a venv tem(comando apenas para agilziar debugs ocasionais) 
call pip list

:: fazer Se não tiver ativado a venv, o comando pip freeze não vai ser executado
call pip freeze > requirements.txt

:: Abre o Google Chrome no endereço http://127.0.0.1:8001/
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" http://127.0.0.1:8001/admin/

python manage.py runserver 8001
