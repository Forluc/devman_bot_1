# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt pip3 install -r requirements.txt

COPY . .

CMD [ "python", "main.py"]

EXPOSE 3000