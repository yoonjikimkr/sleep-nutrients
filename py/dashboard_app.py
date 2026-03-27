import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os

# --- Page Configurations ---
st.set_page_config(
    page_title="식물성 멜라토닌 시장 전략 대시보드",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Light Mode) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto+Sans+KR', sans-serif;
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    .stApp {
        background: #f8fafc;
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: #1e1b4b;
        margin-bottom: 1rem;
        border-left: 10px solid #4f46e5;
        padding-left: 20px;
    }
    
    .card {
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    .insight-box {
        background: #fdf2f8;
        border-left: 4px solid #db2777;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 0.95rem;
        color: #831843;
    }
    
    .script-box {
        background: #f0f9ff;
        border-left: 4px solid #0284c7;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-style: italic;
        font-size: 0.9rem;
        color: #0c4a6e;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #4f46e5;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
    }
    
    .github-link {
        color: #4f46e5;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    h3 {
        color: #1e1b4b;
        font-weight: 800;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Constants & Links ---
GITHUB_BASE = "https://github.com/yoonjikimkr/sleep-nutrients/blob/main/"

# --- Data Loading ---
@st.cache_data
def load_trends():
    df = pd.read_csv('data/naver_datalab_trends.csv', encoding='utf-8-sig')
    if 'period' in df.columns:
        df['date'] = pd.to_datetime(df['period'])
    return df

@st.cache_data
def load_products():
    conn = sqlite3.connect('data/melatonin_topproducts.db')
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df

# --- Sidebar ---
st.sidebar.markdown("<h2 style='text-align: center; color: #4f46e5;'>🌙 Market Strategy</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "메뉴 이동",
    ["1. 시장 개요 및 트렌드", "2. 데이터 기반 시장 분석", "3. 타겟 페르소나 및 전략", "4. 분석 데이터 및 소스코드"]
)

st.sidebar.markdown("---")
st.sidebar.info("본 대시보드는 수면 장애를 겪는 4050 타겟을 위해, 데이터 기반의 '프리미엄 식물성 멜라토닌' 신규 PB 상품 기획 및 시장 안착 전략을 제시합니다.")

# --- Main Logic ---
if menu == "1. 시장 개요 및 트렌드":
    st.markdown("<h1 class='main-title'>시장 개요 및 성장 트렌드</h1>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='card text-center'><div class='metric-label'>글로벌 시장규모 (2031 전망)</div><div class='metric-value'>$3.22B</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card text-center'><div class='metric-label'>연평균 성장률(CAGR)</div><div class='metric-value'>9.28%</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card text-center'><div class='metric-label'>분석 대상 로우 데이터</div><div class='metric-value'>80개</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='card text-center'><div class='metric-label'>핵심 타겟 Demographic</div><div class='metric-value'>4050대</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='script-box'>\"현재 글로벌 멜라토닌 시장은 2031년까지 약 32억 달러 규모로 성장이 예상되며, 특히 한국 시장은 수면장애 환자 급증에 따른 폭발적 수요가 감지되고 있습니다.\"</div>", unsafe_allow_html=True)

    # Search Trend
    st.markdown("<div class='card'><h3>📈 '멜라토닌' 검색 관심도 (네이버 데이터랩 API)</h3>", unsafe_allow_html=True)
    df_trends = load_trends()
    fig_trend = px.line(df_trends, x='date', y='멜라토닌', title='최근 2년간 월간 검색량 추이',
                        template='plotly_white', color_discrete_sequence=['#6366f1'])
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='insight-box'>
    <b>Strategic Insight:</b> 2024년 초 식물성 멜라토닌의 법적 판매 기반이 마련되면서 일반 소비자들의 자발적 검색량이 3배 이상 급증했습니다. 이는 '대기 수요'가 이미 충분함을 의미합니다.
    </div>
    """, unsafe_allow_html=True)

elif menu == "2. 데이터 기반 시장 분석":
    st.markdown("<h1 class='main-title'>시장 지형도 및 정량 데이터 분석</h1>", unsafe_allow_html=True)
    df_products = load_products()
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("<div class='card'><h3>💊 제형별 점유율 (Formulation)</h3>", unsafe_allow_html=True)
        fig_pie = px.pie(names=['정제/캡슐', '구미/젤리', '파우더/분말'], values=[81, 13, 5], 
                         title='네이버/SSG 80개 상위 제품군 분석', hole=0.4, template='plotly_white',
                         color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("<div class='insight-box'><b>Gap Analysis:</b> 현재 시장의 81%가 약 형태인 정제입니다. 하지만 소비자 리뷰 분석 결과 '구미' 제형에 대한 선호도가 월등히 높게 나타납니다.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_b:
        st.markdown("<div class='card'><h3>🍒 시너지 원료 중요도 (TF-IDF)</h3>", unsafe_allow_html=True)
        fig_ing = px.bar(x=['테아닌', '트립토판', '마그네슘', '비타민', 'GABA'], 
                        y=[18, 18, 15, 13, 10],
                        title='제품명 및 홍보문구 텍스트 마이닝 결과', 
                        template='plotly_white', color_discrete_sequence=['#06b6d4'])
        st.plotly_chart(fig_ing, use_container_width=True)
        st.markdown("<div class='script-box'>\"단순 멜라토닌 함량 경쟁보다는 테아닌, 트립토판 등 수면 시너지를 극대화하는 성분 배합이 소비자 구매 결정의 핵심 요인으로 분석되었습니다.\"</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><h3>💰 가격 및 리뷰 상관관계 분석</h3>", unsafe_allow_html=True)
    # Ensure no NaNs in columns used for plotting
    df_plot = df_products.copy()
    df_plot['review_score'] = df_plot['review_score'].fillna(0)
    df_plot['review_count'] = df_plot['review_count'].fillna(0)
    df_plot['discounted_price'] = df_plot['discounted_price'].fillna(0)
    
    fig_corr = px.scatter(df_plot, x='review_count', y='discounted_price', size='review_score',
                         title='80개 상위 제품 가격-성능 지표 (Scatter)',
                         labels={'review_count': '시장 검증(리뷰)', 'discounted_price': '가격(원)'},
                         template='plotly_white', color='review_score', color_continuous_scale='Bluered')
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "3. 타겟 페르소나 및 전략":
    st.markdown("<h1 class='main-title'>타겟 페르소나 및 신제품 전략</h1>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns([1, 1.4])
    
    with col_t1:
        st.markdown("""
        <div class='card'>
        <h3>👤 핵심 타겟: 4050 전문직군</h3>
        <p>사회적 책임이 가장 큰 연령층이며, 생물학적인 멜라토닌 분비 저하와 사회적 스트레스가 결합된 <b>가장 절실한 고객층</b>입니다.</p>
        <hr style='border: 0.5px solid #e2e8f0;'>
        <ul>
            <li><b>Persona A (High Value):</b> 고가 시너지 성분 민감.</li>
            <li><b>Persona B (Continuous):</b> 갱년기 관리 및 정기 구독형.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if os.path.exists('data/chart_4050_persona_clusters.png'):
            st.image('data/chart_4050_persona_clusters.png', caption='HIRA 공공데이터 기반 K-Means 클러스터링 결과')
        
    with col_t2:
        st.markdown("""
        <div class='card' style='border-top: 8px solid #4f46e5;'>
        <h2 style='margin-top: 0;'>✨ 전략 제안: 미드나잇 하모니</h2>
        <p><i>"전문가를 위한 프리미엄 식물성 멜라토닌 솔루션"</i></p>
        <hr style='border: 0.5px solid #e2e8f0;'>
        <table style='width: 100%; border-collapse: collapse; font-size: 0.95rem;'>
            <tr><td style='padding: 10px; border-bottom: 1px solid #f1f5f9;'><b>Formulation</b></td><td style='padding: 10px; border-bottom: 1px solid #f1f5f9;'>맛있는 프리미엄 구미 (Zero Sugar)</td></tr>
            <tr><td style='padding: 10px; border-bottom: 1px solid #f1f5f9;'><b>Ingredient</b></td><td style='padding: 10px; border-bottom: 1px solid #f1f5f9;'>Tart Cherry + Theanine 200mg + Tryptophan</td></tr>
            <tr><td style='padding: 10px; border-bottom: 1px solid #f1f5f9;'><b>Safety</b></td><td style='padding: 10px; border-bottom: 1px solid #f1f5f9;'>1.5mg Mild Content / Non-GMO</td></tr>
            <tr><td style='padding: 10px; border-bottom: 1px solid #f1f5f9;'><b>Price</b></td><td style='padding: 10px; border-bottom: 1px solid #f1f5f9;'>~1,300원/회 (고가 프리미엄 전략)</td></tr>
            <tr><td style='padding: 10px;'><b>Channel</b></td><td style='padding: 10px;'>SSG/백화점 (신뢰) & Naver/GMarket (경험)</td></tr>
        </table>
        </div>
        <div class='script-box'>\"미드나잇 하모니는 자기 전 부담 없이 먹을 수 있는 무설탕 구미 제형에, 테아닌 200mg의 강력한 진정 효과를 더해 4050 프로페셔널의 수면질을 근본적으로 개선합니다.\"</div>
        """, unsafe_allow_html=True)

elif menu == "4. 분석 데이터 및 소스코드":
    st.markdown("<h1 class='main-title'>Analytics Evidence & Source Code</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
    <h3>📂 Project Repository: <a href='https://github.com/yoonjikimkr/sleep-nutrients' class='github-link'>sleep-nutrients</a></h3>
    <p>본 프로젝트에 사용된 모든 데이터 전처리 코드와 머신러닝 분석 스크립트는 아래 링크에서 확인할 수 있습니다.</p>
    <table style='width: 100%; border-collapse: collapse;'>
        <thead>
            <tr style='background: #f8fafc;'>
                <th style='padding: 12px; text-align: left;'>Type</th>
                <th style='padding: 12px; text-align: left;'>Resource Name</th>
                <th style='padding: 12px; text-align: center;'>GitHub Link</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style='padding: 12px; border-bottom: 1px solid #f1f5f9;'>Analysis Script</td>
                <td style='padding: 12px; border-bottom: 1px solid #f1f5f9;'>4050 Target ML Analysis (K-Means)</td>
                <td style='padding: 12px; border-bottom: 1px solid #f1f5f9; text-align: center;'><a href='{0}py/analyze_4050_public_ml.py' target='_blank' class='github-link'>View Code</a></td>
            </tr>
            <tr>
                <td style='padding: 12px; border-bottom: 1px solid #f1f5f9;'>database</td>
                <td style='padding: 12px; border-bottom: 1px solid #f1f5f9;'>Top 80 Products SQLite DB</td>
                <td style='padding: 12px; border-bottom: 1px solid #f1f5f9; text-align: center;'><a href='{0}data/melatonin_topproducts.db' target='_blank' class='github-link'>Raw Data</a></td>
            </tr>
            <tr>
                <td style='padding: 12px; border-bottom: 1px solid #f1f5f9;'>Dataset</td>
                <td style='padding: 12px; border-bottom: 1px solid #f1f5f9;'>Naver DataLab Trends (CSV)</td>
                <td style='padding: 12px; border-bottom: 1px solid #f1f5f9; text-align: center;'><a href='{0}data/naver_datalab_trends.csv' target='_blank' class='github-link'>Cleaned CSV</a></td>
            </tr>
            <tr>
                <td style='padding: 12px;'>Source Code</td>
                <td style='padding: 12px;'>Streamlit Dashboard App</td>
                <td style='padding: 12px; text-align: center;'><a href='{0}py/dashboard_app.py' target='_blank' class='github-link'>Python App</a></td>
            </tr>
        </tbody>
    </table>
    </div>
    """.format(GITHUB_BASE), unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8rem;'>© 2026 Antigravity Strategy Lab | BA Project | 7:40 PM Slide Notes Synced</p>", unsafe_allow_html=True)
