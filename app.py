import random
from typing import Dict, List, Optional, Set, Tuple

import streamlit as st

# 음식 카테고리와 각 카테고리에 속하는 메뉴 및 맵기 정도 (0: 안매움, 1: 약간 매움, 2: 매움, 3: 아주 매움)
FOOD_CATEGORIES: Dict[str, List[Tuple[str, int]]] = {
    "한식": [
        ("된장찌개", 0),
        ("김치찌개", 2),
        ("비빔밥", 1),
        ("불고기", 0),
        ("갈비탕", 0),
        ("냉면", 0),
        ("비빔냉면", 1),
        ("떡볶이", 2),
        ("제육볶음", 2),
        ("순두부찌개", 1),
        ("삼겹살", 0),
    ],
    "중식": [
        ("짜장면", 0),
        ("짬뽕", 2),
        ("탕수육", 0),
        ("양장피", 0),
        ("마파두부", 2),
        ("볶음밥", 0),
        ("울면", 0),
        ("깐풍기", 1),
        ("유린기", 0),
        ("멘보샤", 0),
    ],
    "일식": [
        ("초밥", 0),
        ("라멘", 0),
        ("돈까스", 0),
        ("우동", 0),
        ("가츠동", 0),
        ("규동", 0),
        ("덮밥", 0),
        ("오코노미야끼", 0),
        ("타코야끼", 0),
        ("소바", 0),
    ],
    "양식": [
        ("파스타", 0),
        ("피자", 0),
        ("햄버거", 0),
        ("스테이크", 0),
        ("샌드위치", 0),
        ("리조또", 0),
        ("오믈렛", 0),
        ("시저샐러드", 0),
        ("타코", 1),
        ("부리또", 1),
    ],
    "베트남음식": [
        ("쌀국수", 0),
        ("월남쌈", 0),
        ("반미", 0),
        ("분짜", 0),
        ("짜조", 0),
        ("반세오", 0),
        ("분보후에", 1),
        ("반컴", 0),
        ("껌승", 0),
    ],
    "태국음식": [
        ("팟타이", 1),
        ("톰얌꿍", 2),
        ("그린커리", 2),
        ("쏨땀", 3),
        ("카오팟", 0),
        ("똠까가이", 2),
        ("카오팟 푸", 0),
        ("팟크라파오", 2),
        ("푸팟퐁커리", 1),
    ],
    "인도음식": [
        ("커리", 1),
        ("탄두리 치킨", 1),
        ("난", 0),
        ("사모사", 1),
        ("티카마살라", 1),
        ("팔락 파니르", 0),
        ("비리야니", 1),
        ("라씨", 0),
        ("라지마", 1),
    ],
    "동남아음식": [
        ("나시고랭", 1),
        ("사테이", 0),
        ("레당", 0),
        ("락사", 1),
        ("미고랭", 1),
        ("아얌 고랭", 1),
        ("롬", 0),
        ("바쿠테", 0),
    ],
}

# 맵기 레벨에 대한 이모지 표시
SPICY_EMOJI = {
    0: "🍽️ (안매움)",
    1: "🌶️ (약간 매움)",
    2: "🌶️🌶️ (매움)",
    3: "🌶️🌶️🌶️ (아주 매움)",
}


def get_all_menus(
    selected_categories: Set[str], spicy_level: List[int]
) -> List[Tuple[str, int]]:
    """
    선택한 카테고리와 맵기 레벨에 맞는 메뉴 목록을 반환합니다.

    Args:
        selected_categories: 선택한 카테고리 집합
        spicy_level: 선택한 맵기 레벨 목록

    Returns:
        선택한 카테고리와 맵기 레벨을 고려한 메뉴 목록
    """
    all_menus: List[Tuple[str, int]] = []

    for category, menus in FOOD_CATEGORIES.items():
        if category in selected_categories:
            all_menus.extend(
                [(menu, spicy) for menu, spicy in menus if spicy in spicy_level]
            )

    return all_menus


def recommend_menu(
    selected_categories: Set[str], spicy_level: List[int]
) -> Optional[Tuple[str, int]]:
    """
    선택한 카테고리와 맵기 레벨을 고려하여 메뉴를 추천합니다.

    Args:
        selected_categories: 선택한 카테고리 집합
        spicy_level: 선택한 맵기 레벨 목록

    Returns:
        추천된 메뉴와 맵기 정도
    """
    available_menus = get_all_menus(selected_categories, spicy_level)

    if not available_menus:
        return None

    return random.choice(available_menus)


def main() -> None:
    st.set_page_config(page_title="점심 메뉴 추천", page_icon="🍱")

    st.title("🍱 오늘 점심 뭐 먹지?")
    st.write(
        "먹고 싶은 음식 카테고리를 선택하고 원하는 맵기 정도를 선택한 후 '메뉴 추천받기' 버튼을 눌러보세요!"
    )

    # 카테고리 선택
    st.subheader("먹고 싶은 카테고리 선택")

    categories = list(FOOD_CATEGORIES.keys())

    # 모든 카테고리 선택/해제 버튼 - 중앙에 좌우로 나란히 배치
    col_left, col_select, col_deselect, col_right = st.columns([1, 1, 1, 1])
    with col_select:
        if st.button("모두 선택", key="select_all", use_container_width=True):
            for category in categories:
                st.session_state[f"{category}_selected"] = True
    with col_deselect:
        if st.button("모두 해제", key="deselect_all", use_container_width=True):
            for category in categories:
                st.session_state[f"{category}_selected"] = False

    selected_categories: Set[str] = set()
    col1, col2 = st.columns(2)
    half = len(categories) // 2

    with col1:
        for category in categories[:half]:
            # 초기 상태 설정 (세션 상태에 없으면 기본값은 True)
            if f"{category}_selected" not in st.session_state:
                st.session_state[f"{category}_selected"] = True

            # 체크박스 생성 (value 파라미터는 사용하지 않고 세션 상태만 사용)
            if st.checkbox(
                f"{category}",
                key=f"{category}_selected",
            ):
                selected_categories.add(category)

    with col2:
        for category in categories[half:]:
            # 초기 상태 설정 (세션 상태에 없으면 기본값은 True)
            if f"{category}_selected" not in st.session_state:
                st.session_state[f"{category}_selected"] = True

            # 체크박스 생성 (value 파라미터는 사용하지 않고 세션 상태만 사용)
            if st.checkbox(
                f"{category}",
                key=f"{category}_selected",
            ):
                selected_categories.add(category)

    # 맵기 선택 옵션 추가
    st.subheader("🌶️ 맵기 선택")
    spicy_col1, spicy_col2 = st.columns(2)

    with spicy_col1:
        spicy_options = {
            0: st.checkbox("안매움", value=True, key="spicy_0"),
            1: st.checkbox("약간 매움", value=True, key="spicy_1"),
        }

    with spicy_col2:
        spicy_options.update(
            {
                2: st.checkbox("매움", value=True, key="spicy_2"),
                3: st.checkbox("아주 매움", value=True, key="spicy_3"),
            }
        )

    spicy_level = [level for level, selected in spicy_options.items() if selected]

    if not spicy_level:
        st.warning("최소한 하나의 맵기 옵션을 선택해주세요!")
        spicy_level = [0]  # 기본값으로 안매움 선택
        spicy_options[0] = True

    # 메뉴 추천 버튼 (가운데 정렬)
    left_col, center_col, right_col = st.columns([1, 2, 1])
    with center_col:
        if st.button("메뉴 추천받기", use_container_width=True):
            recommendation = recommend_menu(selected_categories, spicy_level)

            if recommendation is None:
                st.error(
                    "선택한 조건에 맞는 메뉴가 없습니다. 다른 옵션을 선택해주세요!"
                )
            else:
                menu_name, spicy = recommendation
                st.success(f"## 오늘의 추천 메뉴: {menu_name}")

                # 맵기 표시
                st.markdown(f"**맵기**: {SPICY_EMOJI[spicy]}")

                # 카테고리 찾기
                menu_category = None
                for category, menus in FOOD_CATEGORIES.items():
                    menu_names = [m[0] for m in menus]
                    if menu_name in menu_names:
                        menu_category = category
                        break

                if menu_category:
                    st.info(f"**카테고리**: {menu_category}")

            # 다시 추천받기 버튼 활성화
            st.session_state.show_again = True

    # 다시 추천받기 버튼 (가운데 정렬)
    if st.session_state.get("show_again", False):
        left_col, center_col, right_col = st.columns([1, 2, 1])
        with center_col:
            if st.button("다른 메뉴 추천받기", use_container_width=True):
                recommendation = recommend_menu(selected_categories, spicy_level)

                if recommendation is None:
                    st.error(
                        "선택한 조건에 맞는 메뉴가 없습니다. 다른 옵션을 선택해주세요!"
                    )
                else:
                    menu_name, spicy = recommendation
                    st.success(f"## 오늘의 추천 메뉴: {menu_name}")

                    # 맵기 표시
                    st.markdown(f"**맵기**: {SPICY_EMOJI[spicy]}")

                    # 카테고리 찾기
                    menu_category = None
                    for category, menus in FOOD_CATEGORIES.items():
                        menu_names = [m[0] for m in menus]
                        if menu_name in menu_names:
                            menu_category = category
                            break

                    if menu_category:
                        st.info(f"**카테고리**: {menu_category}")


if __name__ == "__main__":
    main()
