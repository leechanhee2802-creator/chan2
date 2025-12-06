"""Streamlit 기반 식단 관리 앱."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List

import streamlit as st


# Ensure local modules are importable when the working directory differs (e.g., Streamlit Cloud)
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from nutrition import FOODS, summarize_with_missing


st.set_page_config(page_title="식단 관리", page_icon="🥗", layout="wide")
st.title("🥗 식단 영양 정보 조회")
st.write("한글 음식 이름을 선택하거나 입력하면 1회 제공량 기준 칼로리와 3대 영양소를 보여줍니다.")


def _parse_manual_input(raw_text: str) -> List[str]:
    """쉼표나 공백으로 구분된 입력을 리스트로 변환합니다."""
    tokens = re.split(r"[,\s]+", raw_text.strip())
    return [token for token in tokens if token]


with st.sidebar:
    st.header("음식 선택")
    selected_foods = st.multiselect("지원 음식", options=sorted(FOODS.keys()))
    manual_input = st.text_input("추가 음식 입력 (쉼표/공백 구분)")
    submitted = st.button("조회하기")

foods: List[str] = []
foods.extend(selected_foods)
foods.extend(_parse_manual_input(manual_input))

if submitted:
    rows, total, missing = summarize_with_missing(foods)

    if rows:
        st.subheader("영양 정보")
        st.table([
            {
                "음식": row[0],
                "기준량": row[1],
                "칼로리": row[2],
                "단백질": row[3],
                "탄수화물": row[4],
                "지방": row[5],
            }
            for row in rows
        ])

        st.success(
            f"총합: {total.calories} kcal · 단백질 {total.protein:.1f} g · "
            f"탄수화물 {total.carbs:.1f} g · 지방 {total.fat:.1f} g"
        )
    else:
        st.warning("알려진 음식이 없습니다. 좌측 목록에서 선택하거나 이름을 다시 입력해 보세요.")

    if missing:
        st.divider()
        st.subheader("확인이 필요한 입력")
        for name, suggestions in missing:
            if suggestions:
                st.info(f"'{name}'을(를) 찾을 수 없습니다. 혹시 {', '.join(suggestions)} 중 하나인가요?")
            else:
                st.error(f"'{name}'을(를) 찾을 수 없습니다. 지원 음식 목록을 확인해주세요.")
else:
    st.info("좌측 사이드바에서 음식 이름을 선택하거나 입력한 뒤 '조회하기'를 눌러주세요.")
