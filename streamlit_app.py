import streamlit as st
import random
import time

# --- 1. 화면 기본 설정 ---
st.set_page_config(page_title="랜덤 코디 자판기", page_icon="🛍️", layout="centered")

# --- 2. 데이터 정의 (가격 및 카테고리 고정) ---
ITEM_PRICE = 50000

CODI_DATA = {
    "귀여운": [
        "🧸 퍼프 소매 블라우스 + 멜빵 원피스 + 미니 백",
        "🐰 오버핏 후드티 + 플리츠 스커트 + 레그 워머"
    ],
    "시크한": [
        "😎 오버핏 가죽 자켓 + 와이드 슬랙스 + 실버 숄더백",
        "🖤 블랙 크롭 탑 + 카고 팬츠 + 볼드한 체인 목걸이"
    ],
    "단정한": [
        "🤍 트위드 자켓 + A라인 스커트 + 진주 귀걸이",
        "👔 테일러드 셔츠 + 슬림핏 슬랙스 + 가죽 로퍼"
    ]
}

# --- 3. 세션 상태(Session State) 초기화 ---
if "cart" not in st.session_state:
    st.session_state.cart = []
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False
if "final_result" not in st.session_state:
    st.session_state.final_result = ""

# --- 4. 메인 화면 타이틀 및 안내 (st.write 사용) ---
st.title("🛍️ 랜덤 코디 뽑기 자판기")
st.write("원하는 스타일 카테고리를 장바구니에 담고 결제해보세요!")
st.write(f"결제 시 장바구니에 담긴 카테고리 중 **하나의 코디 세트가 랜덤으로 매칭**되어 배송됩니다. (모든 카테고리 단일가 {ITEM_PRICE:,}원)")
st.write("---")

# --- 5. 화면 분기 (결제 완료 vs 메인 쇼핑 화면) ---
if st.session_state.payment_done:
    # [결제 완료 페이지] - st.success와 st.info로 결과 출력
    st.success("💳 결제가 성공적으로 완료되었습니다!")
    st.balloons()
    
    st.subheader("🎉 오늘의 랜덤 코디 결과 🎉")
    st.info(f"✨ **{st.session_state.final_result}** ✨ 스타일이 당첨되었습니다! 예쁘게 입으세요!")
    
    # 다시 쇼핑하기 (위젯 상태 초기화 및 화면 리프레시)
    if st.button("다시 쇼핑하기"):
        st.session_state.cart = []
        st.session_state.payment_done = False
        st.session_state.final_result = ""
        st.rerun()

else:
    # [메인 쇼핑 페이지]
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.subheader("🔍 카테고리 선택")
        
        # 👉 [Input 위젯] st.selectbox를 활용해 사용자 선택값 입력받기
        selected_category = st.selectbox(
            "어떤 스타일을 후보에 넣으시겠어요?", 
            options=list(CODI_DATA.keys())
        )
        
        # 👉 [Output 위젯] 선택한 결과에 따른 가격 정보를 st.write로 실시간 표시
        st.write(f"💰 해당 카테고리 가격: **{ITEM_PRICE:,}원**")
        
        # 장바구니 추가 버튼 클릭 시 로직 처리
        if st.button("🛒 장바구니에 추가"):
            if selected_category not in st.session_state.cart:
                st.session_state.cart.append(selected_category)
                st.toast(f"'{selected_category}' 스타일이 장바구니에 담겼습니다!")
            else:
                st.warning("이미 장바구니에 담긴 카테고리입니다.")

    with col2:
        st.subheader("🛒 내 장바구니")
        
        # 👉 [Output 위젯] 장바구니 상태를 화면에 조건별로 다르게 출력
        if not st.session_state.cart:
            st.write("장바구니가 비어 있습니다.")
        else:
            # 현재 담긴 아이템 목록을 st.write로 깔끔하게 리스트업
            for item in st.session_state.cart:
                st.write(f"- **{item}** 스타일 ({ITEM_PRICE:,}원)")
            
            # 장바구니 비우기 버튼
            if st.button("장바구니 비우기"):
                st.session_state.cart = []
                st.rerun()

    st.write("---")
    
    # --- 6. 결제 및 랜덤 뽑기 구역 ---
    st.subheader("💳 주문서 작성")
    
    if len(st.session_state.cart) == 0:
        st.warning("카테고리를 최소 1개 이상 장바구니에 담아주세요.")
    else:
        # 데이터 비즈니스 로직 연산 (Input 기반 결과 계산)
        total_price = len(st.session_state.cart) * ITEM_PRICE
        
        # 👉 [Output 위젯] 계산된 총 수량과 금액을 마크다운 스타일 스타일로 화면에 출력
        st.write(f"선택한 카테고리 수: **{len(st.session_state.cart)}개**")
        st.write(f"### 총 결제 금액: :red[{total_price:,}원]")
        
        # 최종 결제 및 랜덤 선택 트리거 버튼
        if st.button(f"✨ {total_price:,}원 결제하고 랜덤 코디 뽑기 ✨", type="primary"):
            
            # [핵심 로직] 장바구니 내부에서 랜덤 추출
            chosen_category = random.choice(st.session_state.cart)
            chosen_items = random.choice(CODI_DATA[chosen_category])
            
            # 시각적 피드백 효과
            with st.spinner("📦 스타일 박스를 무작위로 매칭하고 있습니다..."):
                time.sleep(2)
            
            # 결과 저장 후 상태 변경하여 화면 전환 유도
            st.session_state.final_result = f"[{chosen_category} 스타일] {chosen_items}"
            st.session_state.payment_done = True
            st.rerun()