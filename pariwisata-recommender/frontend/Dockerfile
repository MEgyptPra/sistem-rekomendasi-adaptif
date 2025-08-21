# Gunakan image node versi stabil
FROM node:18

WORKDIR /app

# Salin file dependency dan install
COPY package*.json ./
RUN npm install

# Salin semua source code
COPY . .

# Build aplikasi (output ke folder dist)
RUN npm run build

# Install serve untuk hosting file statis
RUN npm install -g serve

EXPOSE 3000

# Jalankan serve untuk hasil build (production)
CMD ["serve", "-s", "dist", "-l", "3000"]