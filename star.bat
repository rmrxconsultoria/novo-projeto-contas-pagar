@echo off
echo ========================================
echo 🚀 INICIANDO NOVO PROJETO - LOCAL
echo ========================================
echo.

REM Verificar ambiente virtual
if not exist "venv_novoprojeto" (
    echo ❌ Ambiente virtual nao encontrado!
    echo Criando ambiente virtual...
    python -m venv venv_novoprojeto
    echo ✅ Ambiente virtual criado.
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv_novoprojeto\Scripts\activate

REM Verificar dependencias
if not exist "requirements.txt" (
    echo ❌ Arquivo requirements.txt nao encontrado!
    pause
    exit /b 1
)

REM Instalar/atualizar dependencias
echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

REM Verificar porta
echo Verificando porta 8599...
netstat -ano | findstr :8599 > nul
if %errorlevel% equ 0 (
    echo ⚠️  Porta 8599 esta em uso!
    echo Tentando outra porta...
    set PORTA=8600
) else (
    set PORTA=8599
)

REM Iniciar aplicacao
echo.
echo ========================================
echo 🌐 APLICACAO INICIANDO...
echo URL: http://localhost:%PORTA%
echo ========================================
echo.
echo 📌 Pressione Ctrl+C para parar
echo.

streamlit run app.py --server.port %PORTA% --server.headless false
pause