FROM python:3.11-slim

WORKDIR /app

# Копируем всё из папки app в контейнер
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Запускаем без префикса app.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]