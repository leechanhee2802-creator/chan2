from __future__ import annotations

from dataclasses import dataclass
from difflib import get_close_matches
from typing import Dict, Iterable, List, Tuple


@dataclass
class FoodInfo:
    """한 음식의 영양 정보를 담는 자료형"""
    calories: float   # kcal
    protein: float    # g
    carbs: float      # g
    fat: float        # g
    unit: str = "1회 제공량"

    def as_row(self, name: str) -> List[str]:
        """표에 넣기 좋은 형태로 변환"""
        return [
            name,
            self.unit,
            f"{self.calories:.1f}",
            f"{self.carbs:.1f}",
            f"{self.protein:.1f}",
            f"{self.fat:.1f}",
        ]


# ✅ 여기 FOODS 사전은 예시 값이야. 필요하면 숫자/품목은 나중에 바꿔도 됨.
FOODS: Dict[str, FoodInfo] = {
    "고구마": FoodInfo(calories=130, protein=2.0, carbs=30.0, fat=0.2, unit="100g"),
    "닭가슴살": FoodInfo(calories=165, protein=31.0, carbs=0.0, fat=3.6, unit="100g"),
    "브로콜리": FoodInfo(calories=34, protein=2.8, carbs=7.0, fat=0.4, unit="100g"),
    "현미밥": FoodInfo(calories=150, protein=3.0, carbs=32.0, fat=1.0, unit="100g"),
    "백미밥": FoodInfo(calories=155, protein=3.0, carbs=34.0, fat=0.3, unit="100g"),
    "바나나": FoodInfo(calories=89, protein=1.1, carbs=23.0, fat=0.3, unit="1개(100g)"),
}


def lookup_food(name: str) -> Tuple[FoodInfo | None, List[str]]:
    """
    음식 이름으로 FOODS에서 찾아서 반환.
    - 정확히 존재하면 (FoodInfo, []) 반환
    - 없으면 (None, 비슷한 이름 추천 리스트) 반환
    """
    key = name.strip()

    if key in FOODS:
        return FOODS[key], []

    # 비슷한 이름 추천
    suggestions = get_close_matches(key, FOODS.keys(), n=3, cutoff=0.6)
    return None, suggestions


def summarize(foods: Iterable[str]) -> Tuple[List[List[str]], FoodInfo]:
    """
    여러 음식 이름을 받아서
    - 각 음식의 행(row) 리스트
    - 총합 FoodInfo
    를 반환.
    (이 함수는 단순 합산용, 없는 음식은 무시)
    """
    rows: List[List[str]] = []
    total_calories = 0.0
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0

    for food in foods:
        info, _ = lookup_food(food)
        if not info:
            # 없는 음식은 여기서는 그냥 건너뜀
            continue

        rows.append(info.as_row(food))
        total_calories += info.calories
        total_protein += info.protein
        total_carbs += info.carbs
        total_fat += info.fat

    total = FoodInfo(
        calories=total_calories,
        protein=total_protein,
        carbs=total_carbs,
        fat=total_fat,
        unit="총합",
    )

    return rows, total


def summarize_foods(
    foods: Iterable[str],
) -> Tuple[List[List[str]], FoodInfo, List[Tuple[str, List[str]]]]:
    """
    Streamlit 앱에서 쓰는 함수.

    반환값:
    - rows: 화면에 보여줄 표 한 줄씩
    - total: 총합 FoodInfo
    - missing: [(입력한 원래 이름, [비슷한 추천 이름들...]), ...]
    """
    rows: List[List[str]] = []
    missing: List[Tuple[str, List[str]]] = []

    total_calories = 0.0
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0

    for raw_name in foods:
        name = raw_name.strip()
        if not name:
            continue

        info, suggestions = lookup_food(name)
        if not info:
            # 찾지 못한 음식은 missing 목록에 추가
            missing.append((name, suggestions))
            continue

        rows.append(info.as_row(name))
        total_calories += info.calories
        total_protein += info.protein
        total_carbs += info.carbs
        total_fat += info.fat

    total = FoodInfo(
        calories=total_calories,
        protein=total_protein,
        carbs=total_carbs,
        fat=total_fat,
        unit="총합",
    )

    return rows, total, missing