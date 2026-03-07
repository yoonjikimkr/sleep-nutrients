import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="HIRA 수면장애(F51) 분석 대시보드", layout="wide")

# 데이터 로드 (캐싱 적용)
@st.cache_data
def load_data():
    df = pd.read_csv('f51_target_merged.csv')
    # 연도를 문자열에서 숫자로 변환하여 정렬 용이하게 함 (필요시)
    df['연도'] = df['연도'].astype(str)
    return df

df = load_data()

# 사이드바 필터
st.sidebar.header("🔍 분석 필터")
years = sorted(df['연도'].unique())
selected_years = st.sidebar.multiselect("연도 선택", years, default=years)

genders = df['성별'].unique()
selected_genders = st.sidebar.multiselect("성별 선택", genders, default=list(genders))

# 데이터 필터링
mask = df['연도'].isin(selected_years) & df['성별'].isin(selected_genders)
df_filtered = df[mask]

# 메인 타이틀
st.title("🌙 수면장애(F51) 진료 데이터 분석 대시보드")
st.markdown("심평원 데이터를 바탕으로 한 성별/연령대별 수면장애 환자 추이 및 비용 분석")

# 상단 지표 (Metric)
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    total_patients = df_filtered['진료실원수'].sum()
    st.metric("총 진료 실원수", f"{total_patients:,.0f}명")
with col_m2:
    total_cost = df_filtered['요양급여비용'].sum()
    st.metric("총 요양급여비용", f"{total_cost/100000000:,.1f} 억원")
with col_m3:
    avg_cost = total_cost / total_patients if total_patients > 0 else 0
    st.metric("1인당 평균 급여비용", f"{avg_cost:,.0f} 원")

st.divider()

# 첫 번째 행: 파이 차트 & 도넛 차트
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 핵심 타겟 (연령대별 환자 비율)")
    # 연령대별 합계 계산
    df_age = df_filtered.groupby('연령대')['진료실원수'].sum().reset_index()
    fig_pie = px.pie(df_age, values='진료실원수', names='연령대', 
                     title=f"선택 연도({', '.join(selected_years)}) 연령대 분포",
                     hole=0, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("👫 성별 진료 인원 비율")
    df_gender = df_filtered.groupby('성별')['진료실원수'].sum().reset_index()
    fig_donut = px.pie(df_gender, values='진료실원수', names='성별', 
                       title="남녀 환자 비율", hole=0.5,
                       color_discrete_sequence=['#3498db', '#e74c3c'])
    st.plotly_chart(fig_donut, use_container_width=True)

st.divider()

# 두 번째 행: 바 차트 & 라인 차트
col3, col4 = st.columns(2)

with col3:
    st.subheader("📊 연령대별 진료 인원 (성별 누적)")
    # 연령대 정렬 (순서 맞추기)
    age_order = sorted(df['연령대'].unique(), key=lambda x: int(x.split('_')[0]) if '_' in x else 90)
    df_age_gender = df_filtered.groupby(['연령대', '성별'])['진료실원수'].sum().reset_index()
    fig_bar = px.bar(df_age_gender, x='연령대', y='진료실원수', color='성별',
                     title="연령대/성별 환자 수 비교",
                     category_orders={"연령대": age_order},
                     barmode='stack')
    st.plotly_chart(fig_bar, use_container_width=True)

with col4:
    st.subheader("📈 연도별 수면장애 환자 증감 추이")
    df_yearly = df_filtered.groupby(['연도', '성별'])['진료실원수'].sum().reset_index()
    fig_line = px.line(df_yearly, x='연도', y='진료실원수', color='성별',
                       title="연도별 환자 수 변화", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# 마지막 행: 로우 데이터 테이블
st.subheader("📄 필터링된 데이터 요약 테이블")
st.dataframe(df_filtered.sort_values(['연도', '진료실원수'], ascending=[False, False]), 
             use_container_width=True)

st.caption("Data Source: 건강보험심사평가원(HIRA) 수면장애(F51) 통계")
