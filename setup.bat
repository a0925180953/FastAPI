@echo off
CHCP 65001 > nul
echo 🚀 您好，正在準備開發環境...
echo --------------------------------------------------

:: 1. 檢查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 找不到 Python，請先安裝 Python 哦！
    pause
    exit /b
)

:: 2. 建立虛擬環境
if not exist venv (
    echo 📦 正在建立虛擬環境 venv...
    python -m venv venv
) else (
    echo ✅ 虛擬環境 venv 已存在，跳過建立步驟。
)

:: 3. 升級 pip 並安裝後端套件
echo 🐍 正在安裝後端套件 (requirements.txt)...
call venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

:: 4. 安裝前端套件
if exist frontend goto npm_install
goto after_npm

:npm_install
echo 安裝 frontend 套件
cd frontend
cmd /c npm install
cd ..
:after_npm

echo ✅ 前端套件已安裝完成。

:: 5. 檢查 .env
if not exist .env (
    echo 📝 正在建立 .env 範本...
    echo OPENAI_API_KEY=your_key_here > .env
    echo GEMINI_API_KEY=your_key_here >> .env
    echo SECRET_KEY=your_secret_key_here >> .env
    echo ⚠️  別忘了去 .env 填入你的 API Key 哦！
)

echo --------------------------------------------------
echo 🎉 環境配置已完成！
echo 您現在可以啟動開發模式開始工作。
echo --------------------------------------------------
pause
