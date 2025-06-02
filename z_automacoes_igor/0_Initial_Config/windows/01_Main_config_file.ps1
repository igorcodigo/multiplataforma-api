# Este script automatiza a configuração inicial de um projeto Django com ambiente virtual em PowerShell
# Ele cria e ativa um ambiente virtual, instala as dependências, executa um script auxiliar para migrações e se auto-exclui ao final da execução.

# Entrar no diretório pai para rodar os comandos la
Set-Location ..
Set-Location ..
Set-Location ..

# Copiar o conteúdo do arquivo .env.example para um novo arquivo .env
Write-Host "Criando arquivo .env a partir do .env.example..."
if (Test-Path ".env.example") {
    Get-Content ".env.example" | Set-Content ".env"
    Write-Host "Arquivo .env criado com sucesso."
    
    # Remover o arquivo .env.example após a cópia
    # Remove-Item ".env.example" -Force
    # Write-Host "Arquivo .env.example removido."
} else {
    Write-Host "Arquivo .env.example não encontrado. Pulando esta etapa."
}

Write-Host "Criando a venv..."
# Passo 2: Criar um ambiente virtual chamado 'venv' neste diretório
python -m venv .venv

# Passo 3: Ativar o ambiente virtual
& ".venv\Scripts\activate.ps1"

Write-Host "Instalando as bibliotecas necessarias a partir do arquivo 'requirements.txt' "
# Passo 2: Criar um ambiente virtual chamado 'venv' neste diretório
pip install -r requirements.txt 

# Chamar o arquivo que cria as primeiras migracoes
# Muda o diretorio para o dretorio onde esta localizado o arquivo atual
Set-Location $PSScriptRoot
# Chamar o arquivo 1_migs_create_SupUser.bat
Start-Process -FilePath ".\config_file_auxiliar.bat"

# Passo 5: Excluir este script apos ser executado
# $scriptPath = $MyInvocation.MyCommand.Path
# Remove-Item $scriptPath -Force

# Write-Host "Script auto-excluido."

# Simular pausa com Read-Host para fins de debug
$null = Read-Host
Write-Host "Pressione Enter para fechar a janela..."

# Desativa o ambiente virtual
deactivate

# Fecha o terminal
Stop-Process -Id $PID