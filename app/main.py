from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
import os
import shutil
import uuid
from pathlib import Path
from sqlalchemy.orm import Session
import subprocess  # ← ДОБАВЛЕНО для Go

from . import models, schemas
from .database import engine, get_db

# Создаём таблицы в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="JSON to CSV Converter")

# Создаём папку для загрузок, если её нет
UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def read_root():
    return {"message": "JSON to CSV Converter API"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload", response_model=schemas.Conversion)
async def upload_file(
        file: UploadFile = File(),
        db: Session = Depends(get_db)
):
    # Проверяем расширение
    if not file.filename.endswith('.json'):
        raise HTTPException(400, "Можно загружать только JSON файлы")

    # Генерируем уникальное имя файла
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.json"

    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Получаем размер файла
    file_size = os.path.getsize(file_path) / (1024 * 1024)  # в MB

    # Сохраняем информацию в БД
    db_conversion = models.Conversion(
        filename=f"{file_id}.json",
        original_filename=file.filename,
        file_id=file_id,
        file_size_mb=round(file_size, 2),
        status="uploaded"
    )
    db.add(db_conversion)
    db.commit()
    db.refresh(db_conversion)

    return db_conversion


@app.get("/conversions", response_model=list[schemas.Conversion])
def get_conversions(db: Session = Depends(get_db)):
    conversions = db.query(models.Conversion).order_by(models.Conversion.created_at.desc()).all()
    return conversions


@app.get("/files/{file_id}", response_model=schemas.Conversion)
def get_file(file_id: str, db: Session = Depends(get_db)):
    file_record = db.query(models.Conversion).filter(models.Conversion.file_id == file_id).first()
    if not file_record:
        raise HTTPException(404, "Файл не найден")
    return file_record


@app.get("/download/{file_id}")
def download_file(file_id: str, db: Session = Depends(get_db)):
    file_record = db.query(models.Conversion).filter(models.Conversion.file_id == file_id).first()
    if not file_record:
        raise HTTPException(404, "Файл не найден")

    file_path = UPLOAD_DIR / file_record.filename
    if not file_path.exists():
        raise HTTPException(404, "Файл не найден на диске")

    return FileResponse(
        path=file_path,
        filename=file_record.original_filename,
        media_type="application/json"
    )


# ========== НОВЫЕ ЭНДПОИНТЫ ДЛЯ GO ==========

@app.post("/convert/{file_id}")
async def convert_file(file_id: str, db: Session = Depends(get_db)):
    # Находим запись в БД
    file_record = db.query(models.Conversion).filter(models.Conversion.file_id == file_id).first()
    if not file_record:
        raise HTTPException(404, "Файл не найден")

    # Пути к файлам
    input_path = UPLOAD_DIR / file_record.filename
    if not input_path.exists():
        raise HTTPException(404, "Файл не найден на диске")

    # Создаём имя для CSV
    csv_filename = f"{file_id}.csv"
    csv_path = UPLOAD_DIR / csv_filename

    # Запускаем Go-конвертер
    try:
        # Путь к конвертеру (из корня проекта)
        converter_path = Path("C:/Projects PY GO/json2csv_converter/converter/converter.exe")

        result = subprocess.run(
            [str(converter_path), str(input_path), str(csv_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise HTTPException(500, f"Ошибка конвертации: {result.stderr}")

    except Exception as e:
        raise HTTPException(500, f"Ошибка запуска конвертера: {str(e)}")

    # Обновляем запись в БД
    file_record.status = "converted"
    file_record.csv_filename = csv_filename
    db.commit()

    return {
        "message": "Конвертация завершена",
        "file_id": file_id,
        "csv_filename": csv_filename
    }


@app.get("/download-csv/{file_id}")
def download_csv(file_id: str, db: Session = Depends(get_db)):
    file_record = db.query(models.Conversion).filter(models.Conversion.file_id == file_id).first()
    if not file_record or not file_record.csv_filename:
        raise HTTPException(404, "CSV файл не найден")

    csv_path = UPLOAD_DIR / file_record.csv_filename
    if not csv_path.exists():
        raise HTTPException(404, "CSV файл не найден на диске")

    # Формируем имя для скачивания
    download_name = file_record.original_filename.replace('.json', '.csv')

    return FileResponse(
        path=csv_path,
        filename=download_name,
        media_type="text/csv"
    )