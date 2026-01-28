# Cat Facts Collector - V1 (Heroku)
# Script de execucao automatizada

param(
    [switch]$Setup,
    [switch]$CleanInstall
)

$ErrorActionPreference = "Continue"

# Banner
Clear-Host
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Cat Facts Collector - V1 (Heroku)    " -ForegroundColor Cyan
Write-Host "  API: cat-fact.herokuapp.com          " -ForegroundColor Cyan
Write-Host "  Status: OFFLINE                      " -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Obter caminho do projeto
$scriptDir = $PSScriptRoot
$v1Path = Join-Path $scriptDir "cat_facts_collector\v1_cat_fact_official_2026_01"

if (-not (Test-Path $v1Path)) {
    Write-Host "ERRO: Pasta nao encontrada: $v1Path" -ForegroundColor Red
    Write-Host "Execute este script da raiz do projeto." -ForegroundColor Yellow
    exit 1
}

Set-Location $v1Path
Write-Host "Diretorio: $v1Path" -ForegroundColor Cyan
Write-Host ""

# Limpar instalacao
if ($CleanInstall) {
    Write-Host "Limpando instalacao anterior..." -ForegroundColor Yellow
    if (Test-Path "venv") { Remove-Item "venv" -Recurse -Force }
    if (Test-Path "data") { Remove-Item "data" -Recurse -Force }
    if (Test-Path "logs") { Remove-Item "logs" -Recurse -Force }
    Write-Host "Limpeza concluida!" -ForegroundColor Green
    Write-Host ""
}

# Setup
if ($Setup -or $CleanInstall -or -not (Test-Path "venv")) {
    Write-Host "=== SETUP INICIAL ===" -ForegroundColor Cyan
    Write-Host ""
    
    # Verificar Python
    Write-Host "Verificando Python..." -ForegroundColor Cyan
    $pythonCheck = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERRO: Python nao encontrado!" -ForegroundColor Red
        Write-Host "Instale de: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "OK: $pythonCheck" -ForegroundColor Green
    Write-Host ""
    
    # Criar venv
    if (-not (Test-Path "venv")) {
        Write-Host "Criando ambiente virtual..." -ForegroundColor Cyan
        python -m venv venv
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERRO ao criar venv!" -ForegroundColor Red
            exit 1
        }
        Write-Host "OK: Ambiente virtual criado" -ForegroundColor Green
        Write-Host ""
    }
    
    # Ativar venv
    Write-Host "Ativando ambiente virtual..." -ForegroundColor Cyan
    & "venv\Scripts\Activate.ps1"
    Write-Host "OK: Ambiente ativado" -ForegroundColor Green
    Write-Host ""
    
    # Instalar dependencias
    Write-Host "Instalando dependencias..." -ForegroundColor Cyan
    python -m pip install --upgrade pip
    pip install --only-binary :all: -r requirements.txt
    Write-Host "OK: Dependencias instaladas" -ForegroundColor Green
    Write-Host ""
    
    # Criar .env
    if (-not (Test-Path ".env")) {
        if (Test-Path ".env.example") {
            Copy-Item ".env.example" ".env"
            Write-Host "OK: Arquivo .env criado" -ForegroundColor Green
        }
    }
    
    Write-Host "=== SETUP CONCLUIDO! ===" -ForegroundColor Green
    Write-Host ""
}

# Ativar venv se existir
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
}

# Executar
Write-Host "=== EXECUTANDO EXTRACAO ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "AVISO: Esta API esta OFFLINE!" -ForegroundColor Yellow
Write-Host ""

$start = Get-Date
python src\extract_cat_facts.py
$exitCode = $LASTEXITCODE
$end = Get-Date
$duration = $end - $start

Write-Host ""
Write-Host "=== RESULTADO ===" -ForegroundColor Cyan
Write-Host ""

if ($exitCode -eq 0) {
    Write-Host "SUCESSO: Extracao concluida!" -ForegroundColor Green
    Write-Host "Tempo: $($duration.ToString('mm\:ss'))" -ForegroundColor Cyan
    
    $outputFile = "data\cat_facts_heroku.csv"
    if (Test-Path $outputFile) {
        $lines = (Get-Content $outputFile).Count
        $size = (Get-Item $outputFile).Length / 1KB
        Write-Host "Arquivo: $outputFile" -ForegroundColor Cyan
        Write-Host "Linhas: $lines" -ForegroundColor Cyan
        Write-Host "Tamanho: $([math]::Round($size, 2)) KB" -ForegroundColor Cyan
    }
} else {
    Write-Host "ERRO: Extracao falhou (codigo: $exitCode)" -ForegroundColor Red
    Write-Host "LEMBRE-SE: A API Heroku esta OFFLINE desde 2024" -ForegroundColor Yellow
    Write-Host "Use a V2 (catfact.ninja) que esta funcional!" -ForegroundColor Yellow
}

Write-Host ""
Set-Location $scriptDir
