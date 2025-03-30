# qa_guru_hw_1_3
# FastApi + Python

Микросервис на Python + FastAPI

## Установка проекта

Инструкции по установке

```bash
# Клонировать репозиторий:
git clone https://github.com/valgoncharov/qa_guru_hw_1_2.git

# Установить зависимости:
pip install -r requirements.txt

# Установить переменную APP_URL
Создать в корне проекта файл .env, используя данные из шаблона файла .env.samle.
Указать необходимый url для сервиса FastApi

# Запустить сервис FastApi:
uvicorn main:app --reload
```
## Запуск автотестов с помощью CLI
```bash
# Открыть окно терминала выполнить команду, в зависимости какие тесты необходимо прогнать:
## Запуск автотестов приложения проекта:
pytest ./tests/test_user.py
## Запуск Smoke тестов:
pytest ./tests/test_smoke.py
## Запуск тестов по пагинации:
pytest ./tests/test_pagination.py
```
В рамках проекта на FastAPI доступна функциональность:

## Запрос "Статус приложения" - сервиса:
GET /status

## Запрос на "Просмотр данных всех пользователей" с пагинацией:
GET /users

## Запрос на "Просмотр данных пользователя" указав id пользователя:
GET /users/{user_id}
