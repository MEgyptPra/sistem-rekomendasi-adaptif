# Gunakan image node versi stabil
FROM node:20

WORKDIR /app

# Salin file dependency dan install
COPY package*.json ./
RUN npm install

# Salin semua source code
COPY . .

EXPOSE 5173

# Development mode
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]