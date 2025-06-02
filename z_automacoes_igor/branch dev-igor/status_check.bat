@echo off
cd ..
cd ..
echo Diretorio atual: %cd%
echo ==============================

echo Verificando commits entre HEAD e origin/develop
echo ==============================
@REM git log HEAD..origin/main
git log HEAD..origin/develop

echo ==============================

@REM echo Verificando commits entre HEAD e origin/staging
@REM echo ==============================
@REM git log HEAD..origin/staging

echo ==============================
echo Mostrando detalhes do remote origin 
echo fast-forwardable: isso geralmente significa que voce tem commits locais prontos pra subir, sem conflitos.
echo local out of date: o repositorio remoto tem alteracoes que ainda nao foram puxadas localmente.
echo 
git remote show origin

echo ==============================
echo Verificando status do repositorio Git
echo ==============================
git status
