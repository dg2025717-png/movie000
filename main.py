import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    # 1년간 박스오피스 10위권에 든 영화 216편의 요약표를 불러옵니다
    df = pd.read_csv(DATA_URL)
    # 장르가 세로막대 기호(|)로 여러 개 적힌 영화는 첫 번째 장르만 씁니다
    df["장르"] = df["genre"].str.split("|").str[0]
    return df


df = load_data()

# ── 그래프 1. 장르별 영화 편수 도넛 ──
st.header("1. 장르별 영화 편수 (도넛)")
genre_count = df["장르"].value_counts().reset_index()
genre_count.columns = ["장르", "편수"]

fig = px.pie(
    genre_count,
    names="장르",
    values="편수",
    hole=0.45,  # 가운데 구멍을 뚫어 도넛 모양으로
)
# 조각에 마우스를 올리면 편수와 비율이 보이게 합니다
fig.update_traces(hovertemplate="%{label}<br>%{value}편 (%{percent})<extra></extra>")
st.plotly_chart(fig, width="stretch")

# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note1")

st.divider()
# 앞으로 그래프를 계속 추가할 구역
st.header("2. (다음 그래프를 여기에 추가)")# =================================
# ② 장르 안에 영화가 들어 있는 트리맵
# =================================
st.subheader("② 장르 안에 들어 있는 영화 🎬")

fig2 = px.treemap(
    df,
    path=["genre_main", "movieNm"],
    values="total_audi",
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=650,
    margin=dict(
        t=30,
        b=20,
        l=10,
        r=10
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ---------------------------------
# ② 이 그래프로 알 수 있는 것
# ---------------------------------
with st.container(border=True):
    st.markdown("### 💡 이 그래프로 알 수 있는 것")

    st.write(
        "장르별로 어떤 영화들이 포함되어 있는지와 "
        "영화별 총 관객 규모의 차이를 한눈에 비교할 수 있습니다."
    )

st.divider()
