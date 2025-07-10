import streamlit as st
from googletrans import Translator
import requests
import re

# NAVER API 설정
NAVER_CLIENT_ID = "0100000000c7d84a86165cc4c7de5e41daffa346474d3402b1f9b579e3934550df601c87a8"
NAVER_CLIENT_SECRET = "AQAAAADH2EqGFlzEx95eQdr/o0ZHl1hU4XseJgL9yubEeAnoBQ=="

translator = Translator()

# 브랜드명 리스트
BRAND_KEYWORDS = ["샤오미", "화웨이", "레노버", "카통", "디즈니", "미키", "토마스", "BMW", "벤츠"]

# 브랜드 제거 함수
def remove_brand(text):
    for brand in BRAND_KEYWORDS:
        text = text.replace(brand, "")
    return text.strip()

# 네이버 쇼핑 인기 키워드 가져오기
def get_naver_keywords(category, display=10):
    url = f"https://openapi.naver.com/v1/search/shop.json?query={category}&display={display}&sort=sim"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        items = res.json()["items"]
        keywords = set()
        for item in items:
            title = re.sub(r"<.*?>", "", item["title"])
            for word in title.split():
                if 2 <= len(word) <= 10:
                    keywords.add(word)
        return sorted(list(keywords), key=lambda x: -len(x))[:10]
    else:
        return []

# 상품명 생성 함수
def generate_name(chinese_title, category):
    translated = translator.translate(chinese_title, src='zh-cn', dest='ko').text
    clean = remove_brand(translated)
    keywords = get_naver_keywords(category)
    final_words = [w for w in keywords if w not in clean]
    product_name = clean + " " + " ".join(final_words)
    return product_name[:50]

# Streamlit UI
st.set_page_config(page_title="상품명 자동 생성기 PRO", page_icon="🚀")
st.title("상품명 자동 생성기 PRO")
st.markdown("중국 상품명을 입력하면 자동 번역 + 브랜드 제거 + 네이버 인기 키워드 조합으로 최적 상품명을 생성합니다.")

ch_product = st.text_input("중국어 상품명 입력")
category = st.text_input("카테고리 (예: 헬멧, 공기청정기 등)")

if st.button("상품명 생성"):
    if ch_product and category:
        result = generate_name(ch_product, category)
        st.success(f"✅ 생성된 상품명: {result}")
        st.code(result, language='markdown')
    else:
        st.warning("⚠️ 모든 항목을 입력해주세요.")
