# 🚂 RZD Infrastructure Management System

> Современная система учета и управления объектами инфраструктуры, пересекающимися с железнодорожными путями

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.118+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-Proprietary-yellow.svg)](LICENSE)

## 📋 Описание

Система предназначена для централизованного учета и управления информацией о различных объектах инфраструктуры, которые пересекаются с железнодорожными путями. Приложение обеспечивает полный цикл работы с объектами: создание, поиск, фильтрацию и управление данными.

### 🎯 Основные возможности

- ✅ **Универсальная модель объектов** - единая таблица для всех типов инфраструктуры
- 🔍 **Мощный поиск** - полнотекстовый поиск с фильтрацией по множеству параметров
- 🔐 **Система аутентификации** - JWT-токены и управление пользователями
- 📊 **Гибкая архитектура** - трехслойная архитектура для масштабируемости
- 🗺️ **Геопозиционирование** - координаты объектов в формате WGS84
- 📝 **Специфические данные** - JSON-хранилище для уникальных характеристик каждого типа объекта

## 🏗️ Архитектура

Проект построен на основе **трехслойной архитектуры**:

```
┌─────────────────────────────────────┐
│   Presentation Layer (Routers)      │  ← HTTP запросы/ответы
├─────────────────────────────────────┤
│   Business Logic Layer (Services)   │  ← Бизнес-логика
├─────────────────────────────────────┤
│   Data Access Layer (Repositories)  │  ← Работа с БД
└─────────────────────────────────────┘
```

### Слои архитектуры

- **Presentation Layer** (`app/routers/`) - обработка HTTP-запросов, валидация, маршрутизация
- **Business Logic Layer** (`app/services/`) - бизнес-логика, валидация правил, маппинг данных
- **Data Access Layer** (`app/repositories/`) - работа с базой данных, CRUD-операции

## 🛠️ Технологический стек

| Технология | Версия | Назначение |
|------------|--------|------------|
| **Python** | 3.13+ | Язык программирования |
| **FastAPI** | 0.118+ | Современный веб-фреймворк |
| **SQLAlchemy** | 2.0+ | ORM для работы с БД |
| **SQLite** | - | Реляционная база данных |
| **Pydantic** | - | Валидация данных и схемы |
| **PyJWT** | 2.10+ | JWT-аутентификация |
| **Uvicorn** | 0.37+ | ASGI-сервер |
| **Poetry** | - | Управление зависимостями |

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.13 или выше
- Poetry (для управления зависимостями)

### Установка

1. **Клонируйте репозиторий**
```bash
git clone <repository-url>
cd ржд
```

2. **Установите зависимости**
```bash
poetry install
```

3. **Настройте переменные окружения**

Создайте файл `.env` в корне проекта:
```env
TOKEN_SECRET=your-secret-key-here
DB_URL=sqlite:///./app.db
```

4. **Запустите приложение**
```bash
poetry run dev
```



5. **Откройте в браузере**
- Swagger UI: http://localhost:8080/docs

## 📚 API Документация

### 🔍 Поиск объектов

**Поиск с фильтрами**
```http
POST /search/objects
Content-Type: application/json

{
  "query": "мост",
  "object_types": ["bridge"],
  "owners": ["РЖД Поволжская"],
  "year_from": 1960,
  "year_to": 2020,
  "limit": 20,
  "offset": 0
}
```

**Параметры поиска:**
- `query` (опционально) - текст для полнотекстового поиска (поиск в названии, владельце, описании)
- `object_types`(опционально) - фильтр по типам: `bridge`, `embankment`, `pipeline`, `powerline`, `item`
- `owners` (опционально) - фильтр по владельцам
- `year_from` / `year_to` (опционально) - диапазон годов ввода в эксплуатацию
- `limit` - количество результатов (1-100, по умолчанию 20)
- `offset` - смещение для пагинации


## 📁 Структура проекта

```
app/
├── core/                    # Конфигурация приложения
│   └── config.py           # Настройки
├── db/                      # Работа с базой данных
│   └── session.py          # Сессии SQLAlchemy
├── models/                  # SQLAlchemy модели
│   ├── object.py           # Универсальная модель объектов
│   ├── user.py             # Модель пользователя
│   └── accidents.py        # Модель аварий
├── repositories/            # Data Access Layer
│   ├── base_repository.py  # Базовый репозиторий
│   ├── object_repository.py
│   ├── user_repository.py
│   ├── accident_repository.py
│   └── search_repository.py # Репозиторий поиска
├── routers/                 # Presentation Layer
│   ├── bridges.py          # Роутер мостов
│   ├── embankments.py      # Роутер насыпей
│   ├── pipelines.py        # Роутер трубопроводов
│   ├── powerlines.py       # Роутер ЛЭП
│   ├── items.py            # Роутер элементов
│   ├── search.py           # Роутер поиска
│   ├── users.py            # Роутер пользователей
│   └── accidents.py         # Роутер аварий
├── schemas/                 # Pydantic схемы
│   ├── bridge.py
│   ├── embankment.py
│   ├── pipeline.py
│   ├── powerline.py
│   ├── item.py
│   ├── search.py
│   ├── user.py
│   ├── accidents.py
│   └── geo.py              # Географические схемы
├── services/                # Business Logic Layer
│   ├── object_service.py   # Сервис объектов
│   ├── user_service.py     # Сервис пользователей
│   ├── accident_service.py # Сервис аварий
│   ├── search_service.py   # Сервис поиска
│   ├── mappers.py          # Мапперы для преобразования данных
│   ├── seed.py             # Инициализация тестовых данных
│   └── snils.py            # Валидация СНИЛС
├── auth.py                  # Аутентификация и авторизация
├── permissions.py           # Система прав доступа
├── settings.py              # Настройки приложения
├── main.py                  # Главный файл приложения
└── run.py                   # Точка входа
```
---

**Сделано с ❤️ для РЖД**
