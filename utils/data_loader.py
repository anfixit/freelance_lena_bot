import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def load_directions() -> List[Dict[str, Any]]:
    """Загружает данные направлений из JSON файла."""
    try:
        with open('data/directions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Файл directions.json не найден")
        return []
    except json.JSONDecodeError:
        logger.error("Ошибка при чтении directions.json")
        return []


def get_direction_by_id(directions: List[Dict[str, Any]], direction_id: str) -> Dict[str, Any]:
    """Возвращает направление по ID."""
    return next((d for d in directions if d['id'] == direction_id), None)
