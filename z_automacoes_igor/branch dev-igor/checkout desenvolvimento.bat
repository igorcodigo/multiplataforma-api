@echo off
:: Move para o diretório um nível acima 
cd ..
:: Move para o diretório um nível acima 
cd ..

setlocal

:: Muda para a branch desenvolvimento
:: # Lista as branches locais
git branch  
git checkout dev-igor