# JSON to CSV Converter 🚀

Конвертер JSON-файлов в CSV с использованием **FastAPI** + **Go** + **PostgreSQL** + **Docker**.

## Возможности

- 📤 Загрузка JSON-файлов через REST API
- 🔄 Конвертация JSON → CSV на **Go** (быстро!)
- 💾 Сохранение метаданных в PostgreSQL
- 📊 Просмотр всех конвертаций
- 📥 Скачивание исходного JSON и результата CSV
- 🐳 Полная контейнеризация (Docker Compose)

## Технологии

| Компонент | Технология |
|-----------|------------|
| **Бэкенд** | FastAPI (Python) |
| **База данных** | PostgreSQL + SQLAlchemy + Alembic |
| **Конвертер** | Go (скомпилированный бинарник) |
| **Контейнеризация** | Docker, Docker Compose |

## 🚀 Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone <url-репозитория>
cd json2csv_converter
2. Запустить одной командой
bash
docker-compose up -d --build
3. Открыть в браузере
API: http://localhost:8000

Документация Swagger: http://localhost:8000/docs

4. Остановить
bash
docker-compose down
📡 Эндпоинты API
Метод	Эндпоинт	Описание
GET	/	Приветствие
GET	/health	Проверка здоровья
POST	/upload	Загрузить JSON-файл
GET	/conversions	Список всех конвертаций
GET	/files/{file_id}	Информация о файле
GET	/download/{file_id}	Скачать исходный JSON
POST	/convert/{file_id}	Конвертировать JSON в CSV (Go)
GET	/download-csv/{file_id}	Скачать результат CSV
🔧 Локальный запуск (без Docker)
Python часть
bash
# Виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Установка зависимостей
pip install -r app/requirements.txt

# Запуск
uvicorn app.main:app --reload
Go часть
bash
cd converter
go build -o converter.exe
🐳 Структура Docker
app/Dockerfile — образ для FastAPI

converter/Dockerfile — образ для Go-конвертера (многоступенчатая сборка)

docker-compose.yml — оркестрация всех сервисов

📦 Миграции БД (Alembic)
bash
cd app
alembic revision --autogenerate -m "init"
alembic upgrade head
👨‍💻 Автор
Моррис — [твой GitHub/ссылка]

📄 Лицензия
MIT