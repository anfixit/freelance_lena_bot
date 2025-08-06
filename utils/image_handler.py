import logging
from pathlib import Path

from aiogram.types import FSInputFile

logger = logging.getLogger(__name__)

# Пути к изображениям
IMAGES_PATH = Path("images")
MAIN_IMAGES = IMAGES_PATH / "main"
DIRECTIONS_IMAGES = IMAGES_PATH / "directions"
COURSES_IMAGES = IMAGES_PATH / "courses"
TARIFFS_IMAGES = IMAGES_PATH / "tariffs"


def get_image_path(category: str, image_name: str) -> Path:
    """Получить путь к изображению."""
    category_map = {
        "main": MAIN_IMAGES,
        "directions": DIRECTIONS_IMAGES,
        "courses": COURSES_IMAGES,
        "tariffs": TARIFFS_IMAGES,
    }

    if category not in category_map:
        logger.warning(f"Неизвестная категория изображения: {category}")
        return None

    # Убираем дублирование .jpg если оно уже есть
    if not image_name.endswith('.jpg'):
        image_name = f"{image_name}.jpg"

    image_path = category_map[category] / image_name

    if not image_path.exists():
        logger.warning(f"Изображение не найдено: {image_path}")
        return None

    return image_path


def get_start_image() -> FSInputFile:
    """Получить изображение для стартового экрана."""
    path = get_image_path("main", "start_screen")
    return FSInputFile(path) if path else None


def get_direction_image(direction_id: str) -> FSInputFile:
    """Получить изображение для направления."""
    image_map = {
        "online_specialist": "online_specialist",
        "marketplace_work": "marketplace_work",
        "curator_online_school": "curator_school",
        "task_execution": "task_execution"
    }

    image_name = image_map.get(direction_id)
    if not image_name:
        logger.warning(f"Не найдено соответствие для направления: {direction_id}")
        return None

    path = get_image_path("directions", image_name)
    return FSInputFile(path) if path else None


def get_course_image(course_name: str) -> FSInputFile:
    """Получить изображение для курса."""
    image_map = {
        "Специалист по чат-ботам": "chatbot_specialist",
        "Копирайтер": "copywriter",
        "Нейросети": "ai_neural"
    }

    image_name = image_map.get(course_name)
    if not image_name:
        logger.warning(f"Не найдено соответствие для курса: {course_name}")
        return None

    path = get_image_path("courses", image_name)
    return FSInputFile(path) if path else None


def get_courses_overview_image() -> FSInputFile:
    """Получить изображение для обзора курсов."""
    path = get_image_path("courses", "courses_overview")
    return FSInputFile(path) if path else None


def get_tariffs_image() -> FSInputFile:
    """Получить изображение для тарифов."""
    path = get_image_path("tariffs", "tariffs_payment")
    return FSInputFile(path) if path else None
