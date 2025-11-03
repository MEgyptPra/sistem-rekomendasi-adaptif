# Gunakan image node versi stabil
FROM node:18

WORKDIR /app

# Salin file dependency dan install
COPY package*.json ./
RUN npm install

# Salin semua source code
COPY . .

EXPOSE 3000

# Development mode
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]