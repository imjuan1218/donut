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
# 1. 장르별 영화 편수 비율 (도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 비율")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig_donut = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 편수 분포",
)

fig_donut.update_traces(
    hovertemplate="<b>장르: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.text_area(
    "분석 내용을 작성하세요:",
    placeholder="이 그래프를 통해 알 수 있는 점을 적어보세요.",
    key="insight_1",
)
st.markdown("---")


# -------------------------------------------------------------------
# 2. 장르 내 영화별 총 관객수 (트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객수 분포")

fig_treemap = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객수 (칸 크기 = 총 관객수)",
    color="genre",
)

fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명<extra></extra>"
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.text_area(
    "분석 내용을 작성하세요:",
    placeholder="이 그래프를 통해 알 수 있는 점을 적어보세요.",
    key="insight_2",
)
st.markdown("---")


# -------------------------------------------------------------------
# 3. 총 관객수 분포 (히스토그램)
# -------------------------------------------------------------------
st.subheader("3. 총 관객수 분포 (히스토그램)")

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="영화별 총 관객수 분포",
    labels={"total_audi": "총 관객수", "count": "영화 수"},
)

fig_hist.update_traces(
    hovertemplate="<b>관객수 구간: %{x}</b><br>영화 수: %{y}편<extra></extra>"
)

st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.text_area(
    "분석 내용을 작성하세요:",
    placeholder="이 그래프를 통해 알 수 있는 점을 적어보세요.",
    key="insight_3",
)
st.markdown("---")


# -------------------------------------------------------------------
# 4. 개봉일 스크린수 vs 총 관객수 (산점도)
# -------------------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객수",
    labels={"first_scrn": "개봉일 스크린수", "total_audi": "총 관객수", "genre": "장르"},
)

fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.text_area(
    "분석 내용을 작성하세요:",
    placeholder="이 그래프를 통해 알 수 있는 점을 적어보세요.",
    key="insight_4",
)
st.markdown("---")


# -------------------------------------------------------------------
# 5. 영화 10편 이상 장르의 총 관객수 분포 (박스플롯)
# -------------------------------------------------------------------
st.subheader("5. 영화 10편 이상 장르별 총 관객수 분포 (상자 그림)")

genre_counts_series = df["genre"].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df["genre"].isin(major_genres)]

fig_box = px.box(
    df_filtered,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    points="outliers",
    title="영화 10편 이상 장르별 총 관객수 분포",
    labels={"genre": "장르", "total_audi": "총 관객수"},
)

fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.text_area(
    "분석 내용을 작성하세요:",
    placeholder="이 그래프를 통해 알 수 있는 점을 적어보세요.",
    key="insight_5",
)
st.markdown("---")


# -------------------------------------------------------------------
# 6. 개봉일 스크린수, 총 관객수, 첫 주 관객수의 관계 (버블 차트)
# -------------------------------------------------------------------
st.subheader("6. 개봉일 스크린수, 총 관객수, 첫 주 관객수의 관계 (버블 차트)")

fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=40,
    title="개봉일 스크린수 vs 총 관객수 (버블 크기 = 개봉 첫 주 관객수)",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "first_week_audi": "개봉 첫 주 관객수",
        "genre": "장르",
    },
)

fig_bubble.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객수: %{y:,}명<br>"
        "개봉 첫 주 관객수: %{marker.size:,}명<extra></extra>"
    )
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.text_area(
    "분석 내용을 작성하세요:",
    placeholder="이 그래프를 통해 알 수 있는 점을 적어보세요.",
    key="insight_6",
)
st.markdown("---")


# -------------------------------------------------------------------
# 7. 제작 국가 및 장르별 영화 편수 (선버스트)
# -------------------------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 분포 (선버스트)")

nation_genre_counts = (
    df.groupby(["nation", "genre"]).size().reset_index(name="count")
)

fig_sunburst = px.sunburst(
    nation_genre_counts,
    path=["nation", "genre"],
    values="count",
    title="제작 국가 및 장르별 영화 편수 (안쪽: 국가, 바깥쪽: 장르)",
    color="nation",
)

fig_sunburst.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig_sunburst, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.text_area(
    "분석 내용을 작성하세요:",
    placeholder="이 그래프를 통해 알 수 있는 점을 적어보세요.",
    key="insight_7",
)
st.markdown("---")

# -------------------------------------------------------------------
# 여덟 번째 그래프: 계절별 개봉 영화 편수 및 총 관객수 (막대 그래프)
# -------------------------------------------------------------------
st.subheader("8. 계절별 개봉 영화 편수 및 총 관객수")

# 개봉일(openDt)에서 월 추출 및 계절 파생변수 생성
df_season = df.copy()
df_season["month"] = (
    pd.to_datetime(df_season["openDt"].astype(str), format="%Y%m%d").dt.month
)


def get_season(month):
    if month in [3, 4, 5]:
        return "봄 (3~5월)"
    elif month in [6, 7, 8]:
        return "여름 (6~8월)"
    elif month in [9, 10, 11]:
        return "가을 (9~11월)"
    else:
        return "겨울 (12~2월)"


df_season["season"] = df_season["month"].apply(get_season)

# 계절 순서 정렬을 위한 범주형 데이터 설정
season_order = ["봄 (3~5월)", "여름 (6~8월)", "가을 (9~11월)", "겨울 (12~2월)"]

# 계절별 관객수 합계 및 편수 집계
season_summary = (
    df_season.groupby("season")
    .agg(total_audi=("total_audi", "sum"), movie_count=("movieCd", "count"))
    .reindex(season_order)
    .reset_index()
)

# 막대 그래프 생성 (계절별 총 관객수)
fig_season = px.bar(
    season_summary,
    x="season",
    y="total_audi",
    text="movie_count",
    color="season",
    title="계절별 총 관객수 및 개봉 편수 (막대 위 숫자 = 개봉 편수)",
    labels={
        "season": "계절",
        "total_audi": "총 관객수",
        "movie_count": "개봉 편수",
    },
)

# 마우스 호버 및 막대 위 텍스트 설정
fig_season.update_traces(
    texttemplate="%{text}편",
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>총 관객수: %{y:,}명<br>개봉 편수: %{text}편<extra></extra>",
)

st.plotly_chart(fig_season, use_container_width=True)

st.markdown("---")
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.text_area(
    "분석 내용을 작성하세요:",
    placeholder="이 그래프를 통해 알 수 있는 점을 적어보세요.",
    key="insight_8",
)
st.markdown("---")
