
# Entrar no diretório pai para rodar os comandos la
Set-Location ..
Set-Location ..

# # Muda o diretório para o local onde o script está armazenado
# Set-Location $PSScriptRoot

# Ativa o ambiente virtual (certifique-se de ajustar o caminho do ambiente virtual)
& .\.venv\Scripts\Activate

# Set-Location .. # Muda o diretório para o diretório pai se precisar

$appName = Read-Host -Prompt "Enter the Django app name"

# Cria o novo aplicativo Django
python manage.py startapp $appName

# Espera 3 segundos
Write-Host "Aguardando 3 segundos..."
Start-Sleep -Seconds 3

# Cria arquivos vazios urls.py, serializers.py, e signals.py no novo aplicativo
New-Item -Path ".\$appName\urls.py" -ItemType "file" -Force
New-Item -Path ".\$appName\serializers.py" -ItemType "file" -Force
New-Item -Path ".\$appName\signals.py" -ItemType "file" -Force

# Cria a estrutura de diretórios static/js e static/css
New-Item -Path ".\$appName\static\js" -ItemType "directory" -Force
New-Item -Path ".\$appName\static\css" -ItemType "directory" -Force
New-Item -Path ".\$appName\static\images" -ItemType "directory" -Force

# Cria a estrutura de diretório templatesque pode vir a ser usado
New-Item -Path ".\$appName\templates" -ItemType "directory" -Force

# Adiciona o novo aplicativo à lista INSTALLED_APPS em settings.py
$settingsPath = ".\app\settings.py" # Certifique-se de ajustar este caminho
$content = Get-Content $settingsPath
$installedAppsLine = $content | Select-String -Pattern "INSTALLED_APPS = \["
$index = $content.IndexOf($installedAppsLine.Line) + 1
$newLine = "`t'$appName',"
$content = $content[0..($index-1)] + $newLine + $content[$index..$content.Length]
$content | Set-Content $settingsPath

# Adiciona o diretório estático do novo app à lista STATICFILES_DIRS
$staticFilesDirsLine = $content | Select-String -Pattern "STATICFILES_DIRS = \["
if ($staticFilesDirsLine) {
    $staticFilesDirsIndex = $content.IndexOf($staticFilesDirsLine.Line) + 1
    $staticEntry = "`tBASE_DIR / `"$appName`" / `"static`","
    $content = $content[0..($staticFilesDirsIndex-1)] + $staticEntry + $content[$staticFilesDirsIndex..$content.Length]
    $content | Set-Content $settingsPath
}

exit
