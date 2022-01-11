FROM nginx:latest

# копируем файл настроек для nginx
COPY nginx.conf /etc/nginx/nginx.conf

# копируем все файлы фронта
COPY data data

# переходим в директорию с настройками сервера nginx
WORKDIR /etc/nginx

# запускаем nginx для работы фронта
CMD ["nginx", "-g", "daemon off;"]

