@REM @echo off
cd ..
:: Move para o diretório principal (um nível acima da subpasta "utilitários")

call .venv\Scripts\activate

echo rodando testes
python manage.py test