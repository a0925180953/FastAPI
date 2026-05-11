# 使用輕量級 Python 映像檔
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴 (SQLite 需要的編譯環境等)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製後端程式碼
COPY . .

# 暴露 FastAPI 預設埠
EXPOSE 8000

# 啟動指令
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
