# Телеграм бот уведомляющий о проверке заданий онлайн-курса [Devman](https://dvmn.org)

При отправке проверенного задания от преподавателя, бот уведомляет, что задание проверено и есть ли ошибки.

## Окружение

### Требования к установке

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки
зависимостей:

```bash
pip install -r requirements.txt
```

### Добавление чувствительных данных в `.env`

Создать файл `.env` рядом с `main.py` и добавить следующее:

`DVMN_TOKEN`= Присвоить персональный `API-токен` от сайта [Devman](https://dvmn.org/api/docs/)

`TG_API_TOKEN` = Присвоить `API-токен` телеграм
бота([инструкция](https://robochat.io/docs/kak-sozdat-chat-bota-v-telegram/))

`TG_CHAT_ID` = Присвоить персональный `id телеграма`(можно получить в телеграм у специального
бота [@userinfobot](https://telegram.me/userinfobot))

После заполения данных, можно прочитать файл `.env` можно увидеть примерно следующее:

```bash
$ cat .env
DVMN_TOKEN='0000example0000'
TG_API_TOKEN='11111111:eeeeeeeeeeeeeexample'
TG_CHAT_ID='000000000'
```

## Запуск бота

Запуск на Linux(Python 3) или Windows:

```bash
$ python main.py
```

Пример с передаванием аргумента в CLI:

```bash
$ python main.py --chat_id 000000000
```

## Запуск с помощью [Docker](https://www.docker.com/)(локально)

Зарегистрируйтесь и скачайте [Docker](https://www.docker.com/). [Туториал](https://timeweb.cloud/tutorials/docker/kak-ustanovit-docker-na-ubuntu-22-04) на русском.
Соберите образ контейнера командой:
```bash
$ sudo docker build -t dvmn-bot .
```
Запустите контейнер командой:
```bash
$ sudo docker run --dp 127.0.0.1:3000:3000 -e DVMN_TOKEN=... -e TG_API_TOKEN=...  -e TG_CHAT_ID=... dvmn-bot
```
Сделайте тег для пуша:
```bash
$ sudo docker tag dvmn-bot YOUR-USER-NAME/dvmn-bot
```
Запуште образ на репозиторий [Docker](https://www.docker.com/):
```bash
$ sudo docker push YOUR-USER-NAME/dvmn-bot
```

## Запуск с помощью [Docker](https://www.docker.com/)(на сервере)Скачайте [Docker](https://www.docker.com/). [Туториал](https://timeweb.cloud/tutorials/docker/kak-ustanovit-docker-na-ubuntu-22-04) на русском.
Запустите контейнер:
```bash
$ sudo docker run -dp 0.0.0.0:3000:3000 -e DVMN_TOKEN=... -e TG_API_TOKEN=...  -e TG_CHAT_ID=... YOUR-USER-NAME/dvmn-bot
```
Посмотреть контейнер и образ можно командой:
```bash
$ sudo docker ps && sudo docker images
```

### Цель проекта

Скрипт написан в образовательных целях на онлайн-курсе [Devman](https://dvmn.org)
