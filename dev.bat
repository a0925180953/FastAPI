@echo off
:: 強制使用 UTF-8 編碼顯示

CHCP 65001 > nul
echo 🚀 嘿！野原新之助，全能量開發模式啟動！
echo --------------------------------------------------

:: 確保 logs 資料夾存在
if not exist logs (
    mkdir logs
)

:: 1. 在背景啟動後端
taskkill /F /IM python.exe >nul 2>&1
echo 🐍 正在啟動後端伺服器 (FastAPI)...
@REM start "Backend" cmd /k "call venv\Scripts\activate && uvicorn backend.main:app --reload"
start "Backend" cmd /k "call venv\Scripts\activate && python -m backend.main"
echo --------------------------------------------------


:: 2. 啟動前端 (在目前視窗)
echo ⚡ 正在啟動前端開發環境 (Vite)...
echo 💡 提示：按 Ctrl+C 可以停止前端，後端會在視窗關閉時自動結束
echo 📝 詳細日誌請查看 logs/ 資料夾
echo --------------------------------------------------

cd frontend
npm run dev
