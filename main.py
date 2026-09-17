import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("박스오피스 10위권 내 개봉 영화 216편의 데이터를 시각화합니다.")


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: 세로막대 기호(|)로 분리되어 있는 경우 첫 번째 장르만 추출
    df["genre"] = df["genre"].fillna("미상").apply(lambda x: str(x).split("|")[0])

    return df


df = load_data()

st.divider()

# -------------------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 비율")

# 장르별 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 차트 생성
fig_donut = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 편수 분포",
)

# 마우스 호버 시 편수와 비율 표시 설정
fig_donut.update_traces(
    hovertemplate="<b>장르: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig_donut, use_container_width=True)

# 그래프 해석 안내 영역
st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("어떤 장르의 영화가 박스오피스 상위권에 가장 많이 포함되었는지 전체적인 비중을 한눈에 파악할 수 있습니다.")
st.markdown("---")

