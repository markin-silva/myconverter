# Dockerfile para o Frontend Vue.js

# Build Stage
FROM node:20-alpine as build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Production Stage
FROM nginx:stable-alpine as production-stage

# Copia os arquivos buildados para a pasta padrão do NGINX
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expondo porta padrão HTTP
EXPOSE 80

# Comando padrão para rodar o nginx
CMD ["nginx", "-g", "daemon off;"]
