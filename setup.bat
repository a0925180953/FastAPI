@echo off
CHCP 65001 > nul
echo 🚀 嘿！野原新之助，正在為你準備超強大的開發環境...
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
pip install -r requirements.txt

:: 4. 安裝前端套件
if exist frontend (
    echo 🎨 正在進入前端目錄安裝套件 (npm install)...
    cd frontend
    call npm install
    cd ..
)

:: 5. 檢查 .env
if not exist backend\.env (
    echo 📝 正在建立 backend\.env 範本...
    echo OPENAI_API_KEY=your_key_here > backend\.env
    echo GEMINI_API_KEY=your_key_here >> backend\.env
    echo SECRET_KEY=your_secret_key_here >> backend\.env
    echo ⚠️  別忘了去 backend\.env 填入你的 API Key 哦！
)

echo --------------------------------------------------
echo 🎉 太棒了！野原新之助，環境已經準備好啦！
echo 你現在可以優雅地開啟開發模式，去創造奇蹟吧！🔥
echo --------------------------------------------------
pause
