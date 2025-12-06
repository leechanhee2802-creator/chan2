"""간단한 식단 관리 유틸리티.

한글 음식 이름을 받아서 기본적인 영양 성분(칼로리, 단백질, 탄수화물, 지방)을 반환합니다.
"""
from __future__ import annotations

from dataclasses import dataclass
from difflib import get_close_matches
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class FoodInfo:
    calories: int
    protein: float
    carbs: float
    fat: float
    unit: str

    def as_row(self, name: str) -> List[str]:
        """현재 음식 정보를 테이블 행으로 변환합니다."""
        return [
            name,
            self.unit,
            f"{self.calories} kcal",
            f"{self.protein:.1f} g",
            f"{self.carbs:.1f} g",
            f"{self.fat:.1f} g",
        ]


FOODS: Dict[str, FoodInfo] = {
    "닭가슴살": FoodInfo(calories=165, protein=31.0, carbs=0.0, fat=3.6, unit="100 g"),
    "고구마": FoodInfo(calories=86, protein=1.6, carbs=20.1, fat=0.1, unit="100 g"),
    "현미밥": FoodInfo(calories=320, protein=6.5, carbs=69.0, fat=2.2, unit="1 공기(210 g)"),
    "계란": FoodInfo(calories=72, protein=6.0, carbs=0.4, fat=4.8, unit="1개(50 g)"),
    "두부": FoodInfo(calories=76, protein=8.0, carbs=2.0, fat=4.8, unit="100 g"),
    "연어": FoodInfo(calories=208, protein=20.0, carbs=0.0, fat=13.0, unit="100 g"),
    "아몬드": FoodInfo(calories=170, protein=6.0, carbs=6.0, fat=15.0, unit="30 g"),
    "바나나": FoodInfo(calories=105, protein=1.3, carbs=27.0, fat=0.4, unit="1개(118 g)"),
    "사과": FoodInfo(calories=95, protein=0.5, carbs=25.0, fat=0.3, unit="1개(182 g)"),
    "오트밀": FoodInfo(calories=150, protein=5.0, carbs=27.0, fat=3.0, unit="40 g"),
    "우유": FoodInfo(calories=150, protein=8.0, carbs=12.0, fat=8.0, unit="240 ml"),
    "요거트": FoodInfo(calories=100, protein=9.0, carbs=12.0, fat=0.7, unit="170 g"),
    "현미떡": FoodInfo(calories=120, protein=2.0, carbs=26.0, fat=0.8, unit="1개(60 g)"),
    "삶은감자": FoodInfo(calories=87, protein=2.0, carbs=20.0, fat=0.1, unit="100 g"),
    "브로콜리": FoodInfo(calories=34, protein=2.8, carbs=6.6, fat=0.4, unit="100 g"),
    "시금치": FoodInfo(calories=23, protein=2.9, carbs=3.6, fat=0.4, unit="100 g"),
    "단호박": FoodInfo(calories=49, protein=1.8, carbs=12.0, fat=0.2, unit="100 g"),
    "치킨가슴살캔": FoodInfo(calories=120, protein=26.0, carbs=0.0, fat=1.5, unit="100 g"),
    "참치캔": FoodInfo(calories=198, protein=29.0, carbs=0.0, fat=8.0, unit="100 g"),
    "렌틸콩": FoodInfo(calories=115, protein=9.0, carbs=20.0, fat=0.4, unit="100 g"),
}


def lookup_food(name: str) -> Tuple[Optional[FoodInfo], List[str]]:
    """음식 이름으로 영양 정보를 찾습니다.

    Args:
        name: 찾고 싶은 음식 이름.

    Returns:
        - 영양 정보(FoodInfo) 또는 찾지 못했을 경우 None.
        - 비슷한 이름 제안 목록.
    """
    name = name.strip()
    if not name:
        return None, []

    if name in FOODS:
        return FOODS[name], []

    suggestions = get_close_matches(name, FOODS.keys(), n=3, cutoff=0.6)
    return None, suggestions


def summarize(foods: Iterable[str]) -> Tuple[List[List[str]], FoodInfo]:
    """여러 음식 이름을 받아 테이블과 총합을 계산합니다."""
    rows: List[List[str]] = []
    total_calories = 0
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0

    for food in foods:
        info, _ = lookup_food(food)
        if not info:
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
