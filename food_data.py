import json
import os
from typing import Dict, List, Tuple


def load_json_file(file_path: str) -> List[Dict] | Dict:
    """JSON 파일을 로드합니다."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {file_path} 파일을 찾을 수 없습니다.")
        return []
    except json.JSONDecodeError:
        print(f"Warning: {file_path} 파일의 JSON 형식이 올바르지 않습니다.")
        return []


def load_food_categories() -> Dict[str, List[Tuple[str, int]]]:
    """모든 카테고리의 음식 데이터를 로드합니다."""
    categories = {}

    # 카테고리별 파일 매핑
    category_files = {
        "🇰🇷한식": "data/korean.json",
        "🇨🇳중식": "data/chinese.json",
        "🇯🇵일식": "data/japanese.json",
        "🧑‍🍳양식": "data/western.json",
        "🍖고기구이": "data/grilled_meat.json",
        "🌏동남아음식": "data/southeast_asian.json",
        "🍛인도음식": "data/indian.json",
        "🐟🍖날것": "data/raw.json",
    }

    for category_name, file_path in category_files.items():
        menu_data = load_json_file(file_path)
        if menu_data:
            categories[category_name] = [
                (item["name"], item["spicy_level"]) for item in menu_data
            ]
        else:
            categories[category_name] = []

    return categories


def load_spicy_emoji() -> Dict[int, str]:
    """맵기 이모지 데이터를 로드합니다."""
    emoji_data = load_json_file("data/spicy_emoji.json")
    if emoji_data:
        return {int(k): v for k, v in emoji_data.items()}
    else:
        # 기본값 반환
        return {
            0: "🍽️ (안매움)",
            1: "🌶️ (약간 매움)",
            2: "🌶️🌶️ (매움)",
            3: "🌶️🌶️🌶️ (아주 매움)",
        }


# 데이터 로드
FOOD_CATEGORIES: Dict[str, List[Tuple[str, int]]] = load_food_categories()
SPICY_EMOJI: Dict[int, str] = load_spicy_emoji()
