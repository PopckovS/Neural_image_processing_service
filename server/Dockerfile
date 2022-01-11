FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

# копируем файл с зависимостями
COPY ./requirements.txt .

# устанавливаем зависимости
RUN pip install -r requirements.txt

# копируем все приложение код в контейнер
COPY . .

# запускаем команды для миграций и фикстур
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT [ "./docker-entrypoint.sh" ]