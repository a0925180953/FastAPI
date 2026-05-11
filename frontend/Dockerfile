# 使用 Node.js 映像檔
FROM node:20-slim

# 設定工作目錄
WORKDIR /app

# 複製 package.json 和 lock 檔案
COPY package*.json ./

# 安裝前端套件
RUN npm install

# 複製前端程式碼
COPY . .

# 暴露 Vite 預設埠
EXPOSE 5173

# 啟動開發伺服器，並允許外部存取 (--host)
CMD ["npm", "run", "dev", "--", "--host"]
