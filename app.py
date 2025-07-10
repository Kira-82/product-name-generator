import streamlit as st

st.title("상품명 자동 생성기")
st.write("중국 상품명을 입력하면 네이버 인기 키워드를 기반으로 상품명을 자동 생성합니다.")

china_name = st.text_input("중국어 상품명 입력")
category = st.text_input("카테고리 입력")

if st.button("상품명 생성"):
    st.success(f"🔧 생성된 상품명 예시: {china_name} {category} 고급형 추천모델")
