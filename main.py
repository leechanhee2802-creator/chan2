"""식단 관리 CLI.

예시:
    python main.py 닭가슴살 고구마 브로콜리
"""
from __future__ import annotations

import argparse
from typing import Iterable, List

from nutrition import FOODS, lookup_food, summarize


def format_table(headers: List[str], rows: Iterable[Iterable[str]]) -> str:
    # 간단한 고정 폭 테이블 렌더링
    rows = [list(row) for row in rows]
    widths = [len(header) for header in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(cell))

    def render_line(parts: List[str]) -> str:
        padded = [part.ljust(widths[i]) for i, part in enumerate(parts)]
        return " | ".join(padded)

    divider = "-+-".join("-" * w for w in widths)
    lines = [render_line(headers), divider]
    lines.extend(render_line(row) for row in rows)
    return "\n".join(lines)


def handle_lookup(foods: List[str]) -> None:
    headers = ["음식", "기준량", "칼로리", "단백질", "탄수화물", "지방"]
    rows, total = summarize(foods)

    if rows:
        rows.append(["총합", "-", f"{total.calories} kcal", f"{total.protein:.1f} g", f"{total.carbs:.1f} g", f"{total.fat:.1f} g"])
        print(format_table(headers, rows))
    else:
        print("알려진 음식이 없습니다. --list 옵션으로 지원하는 음식을 확인하세요.")

    for food in foods:
        info, suggestions = lookup_food(food)
        if info:
            continue
        if suggestions:
            suggestion_text = ", ".join(suggestions)
            print(f"\n'{food}'을(를) 찾을 수 없습니다. 혹시 {suggestion_text} 중 하나인가요?")
        else:
            print(f"\n'{food}'을(를) 찾을 수 없습니다. --list 옵션으로 지원 음식 목록을 확인하세요.")


def main() -> None:
    parser = argparse.ArgumentParser(description="한글 음식 이름으로 영양 정보를 알려주는 식단 관리 도구")
    parser.add_argument("foods", nargs="*", help="조회할 음식 이름 (여러 개 입력 가능)")
    parser.add_argument("--list", action="store_true", help="지원하는 음식 목록 표시")
    args = parser.parse_args()

    if args.list:
        print("지원 음식 목록:")
        print(", ".join(sorted(FOODS.keys())))
        return

    if not args.foods:
        parser.error("조회할 음식 이름을 한 개 이상 입력하세요.")

    handle_lookup(args.foods)


if __name__ == "__main__":
    main()
