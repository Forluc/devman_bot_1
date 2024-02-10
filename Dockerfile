# syntax=docker/dockerfile:1

# FROM - родительский образ
FROM python:3.10-slim-buster

# WORKDIR - установка рабочей директории для инструкций RUN, CMD, ENTRYPOINT, COPY и ADD
WORKDIR /app

# RUN - выполнение команды в новом слое на основе текущего образа и фиксация результата
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt pip3 install -r requirements.txt

# COPY - копирование новых файлов и добавление в файловую систему образа по адресу
COPY . .

# CMD - предоставление дефолтных значений исполняемому контейнеру
CMD [ "python", "main.py"]

# EXPOSE - информация о сетевом порте, прослушиваемом контейнером во время выполнения
EXPOSE 3000