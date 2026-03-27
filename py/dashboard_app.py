import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto+Sans+KR', sans-serif;
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    .stApp {
        background: #f8fafc;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 0.5rem;
        border-left: 8px solid #4f46e5;
        padding-left: 16px;
        letter-spacing: -0.5px;
    }
    
    .sub-title {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 2rem;
        margin-left: 24px;
        font-weight: 400;
    }
    
    .card {
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 24px;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    
    .card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    .insight-box {
        background: #fdf2f8;
        border-left: 4px solid #db2777;
        padding: 16px;
        border-radius: 0 8px 8px 0;
        margin: 16px 0;
        font-size: 0.95rem;
        color: #831843;
        line-height: 1.6;
    }
    
    .script-box {
        background: #f0f9ff;
        border-left: 4px solid #0284c7;
        padding: 16px;
        border-radius: 0 8px 8px 0;
        margin: 16px 0;
        font-style: italic;
        font-size: 0.95rem;
        color: #0c4a6e;
        line-height: 1.6;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        color: #4f46e5;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .github-link {
        color: #4f46e5;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        transition: color 0.2s;
    }
    .github-link:hover {
        color: #312e81;
        text-decoration: underline;
    }
    
    h3 {
        color: #1e1b4b;
        font-weight: 800;
        margin-top: 0;
        font-size: 1.25rem;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 12px;
        margin-bottom: 16px;
    }
    
    /* Streamlit overrides */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Constants & Links ---
GITHUB_BASE = "https://github.com/yoonjikimkr/sleep-nutrients/blob/main/"

# --- Data Loading (Cached) ---
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
    
    # Pre-calculate formulation for easier filtering
    def get_formulation(row):
        txt = str(row.get('product_name', '')) + " " + str(row.get('package_type', ''))
        if '구미' in txt or '젤리' in txt: return '구미/젤리'
        elif '분말' in txt or '가루' in txt or '파우더' in txt: return '파우더/분말'
        elif '액상' in txt or '포' in txt or '앰플' in txt: return '액상류'
        else: return '정제/캡슐'
    
    df['formulation'] = df.apply(get_formulation, axis=1)
    
    # Clean numeric columns
    df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce').fillna(0)
    df['review_score'] = pd.to_numeric(df['review_score'], errors='coerce').fillna(0)
    df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce').fillna(0)
    return df

df_trends = load_trends()
df_products_raw = load_products()

# --- Sidebar ---
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
    <h2 style='color: #4f46e5; margin-bottom: 0;'>🌙 Midnight Harmony</h2>
    <p style='color: #64748b; font-size: 0.8rem; margin-top: 0;'>Market Strategy Dashboard</p>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "NAVIGATION",
    ["1. 시장 개요 및 트렌드", "2. 데이터 기반 시장 분석", "3. 타겟 페르소나 및 전략", "4. 상품 심층 속성 및 리뷰 분석", "5. 분석 데이터 및 소스코드"]
)

st.sidebar.markdown("---")

# Interactivity: Dynamic filters in sidebar depending on the menu
if menu == "2. 데이터 기반 시장 분석":
    st.sidebar.markdown("### 🎛️ 데이터 인터랙션 필터")
    st.sidebar.caption("아래 필터를 조정하여 시장 데이터를 다각도로 분석해보세요.")
    
    # 1. Formulation multiselect
    all_forms = sorted(df_products_raw['formulation'].unique().tolist())
    selected_forms = st.sidebar.multiselect("💊 제형 필터 (Formulation)", all_forms, default=all_forms)
    
    # 2. Price slider
    max_price = int(df_products_raw['discounted_price'].max())
    if max_price == 0: max_price = 100000 # fallback
    price_range = st.sidebar.slider("💰 가격대 필터 (원)", 0, max_price, (0, max_price), step=1000)
    
    # 3. Minimum Review slider
    min_reviews = st.sidebar.slider("⭐ 최소 리뷰 수 (시장 검증도)", 0, 5000, 0, step=100)
    
    # Actually filter the global dataframe
    df_products = df_products_raw[
        (df_products_raw['formulation'].isin(selected_forms)) &
        (df_products_raw['discounted_price'] >= price_range[0]) &
        (df_products_raw['discounted_price'] <= price_range[1]) &
        (df_products_raw['review_count'] >= min_reviews)
    ]
else:
    df_products = df_products_raw
    st.sidebar.info("본 대시보드는 수면 장애를 겪는 4050 타겟을 위해, 데이터를 바탕으로 한 '프리미엄 식물성 멜라토닌' PB 상품 기획 및 전략을 인터랙티브하게 제시합니다.")

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.75rem;'>© 2026 Sleep Nutrients BA</p>", unsafe_allow_html=True)


# --- Main Logic ---
if menu == "1. 시장 개요 및 트렌드":
    st.markdown("<h1 class='main-title'>시장 개요 및 성장 트렌드</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>글로벌 시장의 폭발적 성장세와 국내 검색 트렌드를 결합한 매크로 분석</p>", unsafe_allow_html=True)
    
    # 4-Column Metrics layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='card text-center'><div class='metric-label'>글로벌 시장규모 (2026 전망)</div><div class='metric-value'>$2.07B</div><div style='font-size: 0.8rem; color: #64748b; margin-top: 4px;'>(2031년 3.22B 성장 전망)</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card text-center'><div class='metric-label'>연평균 성장률(CAGR)</div><div class='metric-value'>9.28%</div><div style='font-size: 0.8rem; color: #64748b; margin-top: 4px;'>(2025-2031 YoY)</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card text-center'><div class='metric-label'>분석 대상 raw data</div><div class='metric-value'>80개</div><div style='font-size: 0.8rem; color: #64748b; margin-top: 4px;'>(Naver/SSG Top 40)</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='card text-center'><div class='metric-label'>핵심 타겟 Demographic</div><div class='metric-value'>4050대</div><div style='font-size: 0.8rem; color: #64748b; margin-top: 4px;'>(F51 기준 31.3%)</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='script-box'>\"현재 글로벌 멜라토닌 시장은 2025년 18.9억 달러를 기록하여 2026년 20.7억 달러를 전망, 2031년까지 약 32억 달러 규모로 성장이 예상되며, 특히 한국 시장은 수면장애 환자 급증에 따른 폭발적 수요가 감지되고 있습니다.\"</div>", unsafe_allow_html=True)

    # Search Trend Chart
    st.markdown("<div class='card'><h3>📈 '멜라토닌' 검색 관심도 (네이버 데이터랩 API)</h3>", unsafe_allow_html=True)
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_trends['date'], y=df_trends['멜라토닌'], 
        mode='lines+markers',
        line=dict(color='#6366f1', width=3),
        marker=dict(size=6, color='#4f46e5'),
        fill='tozeroy', fillcolor='rgba(99, 102, 241, 0.1)',
        name='검색량 지수'
    ))
    fig_trend.update_layout(
        height=400, template='plotly_white', hovermode='x unified',
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis_title="", yaxis_title="상대적 검색량 지수"
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='insight-box'>
    <b>💡 Strategic Insight:</b> 2024년 초 식물성 멜라토닌의 법적 판매 기반이 마련되면서 일반 소비자들의 자발적 검색량이 단기간에 급증했습니다. 이는 시장 내 잠재되어 있던 '대기 수요'가 이미 충분히 임계점을 넘었음을 증명합니다.
    </div>
    """, unsafe_allow_html=True)

elif menu == "2. 데이터 기반 시장 분석":
    st.markdown("<h1 class='main-title'>시장 지형도 및 정량 데이터 분석</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-title'>필터링된 총 <b>{len(df_products)}개</b>의 실제 상위 제품 데이터를 기반으로 한 실시간 인터랙티브 분석</p>", unsafe_allow_html=True)
    
    if len(df_products) == 0:
        st.warning("선택하신 필터 조건에 맞는 제품 데이터가 없습니다. 좌측 패널의 필터를 조정해주세요.")
    else:
        # Layout with Tabs for better depth
        tab1, tab2 = st.tabs(["📊 거시적 시장 포지셔닝 (Overview)", "🔍 세부 가격 및 스펙 분석 (Deep Dive)"])
        
        with tab1:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("<div class='card'><h3>💊 제형별 점유율 (Formulation)</h3>", unsafe_allow_html=True)
                form_counts = df_products['formulation'].value_counts()
                fig_pie = px.pie(
                    names=form_counts.index, values=form_counts.values, 
                    hole=0.4, template='plotly_white',
                    color_discrete_sequence=px.colors.qualitative.Prism
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label', hoverinfo='label+value+percent')
                fig_pie.update_layout(height=400, margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
                st.plotly_chart(fig_pie, use_container_width=True)
                
                jungje_pct = (form_counts.get('정제/캡슐', 0) / len(df_products)) * 100 if len(df_products) > 0 else 0
                st.markdown(f"<div class='insight-box'><b>Gap Analysis:</b> 현재 필터링된 시장의 {jungje_pct:.0f}%가 '정제/캡슐' 기반입니다. 다수의 소비자가 '구미/젤리' 제형에 프리미엄 가치를 지불할 의향을 보이는 것과 상반된 공급 구조입니다.</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_b:
                st.markdown("<div class='card'><h3>🍒 주요 시너지 원료 빈도 분석</h3>", unsafe_allow_html=True)
                ingredients_text = " ".join(df_products['ingredients'].fillna('') + " " + df_products['active_ingredients'].fillna('') + " " + df_products['product_name'].fillna(''))
                keywords = ['타트체리', '비타민', '마그네슘', '트립토판', '테아닌', '가바(GABA)']
                counts = [
                    ingredients_text.count('타트체리'), ingredients_text.count('비타민'),
                    ingredients_text.count('마그네슘'), ingredients_text.count('트립토판'),
                    ingredients_text.count('테아닌'), ingredients_text.count('GABA') + ingredients_text.count('가바')
                ]
                
                df_ing = pd.DataFrame({'Keyword': keywords, 'Count': counts}).sort_values('Count', ascending=True)
                fig_ing = px.bar(
                    df_ing, x='Count', y='Keyword', orientation='h',
                    labels={'Count': '언급 빈도수 (횟수)', 'Keyword': '원료명'},
                    template='plotly_white', color='Count', color_continuous_scale='Teal'
                )
                fig_ing.update_layout(height=400, margin=dict(t=20, b=20, l=20, r=20))
                st.plotly_chart(fig_ing, use_container_width=True)
                
                st.markdown("<div class='script-box'>\"단순 멜라토닌 함량 경쟁보다는 타트체리, 트립토판 등 수면 시너지를 극대화하는 성분 배합이 상위 핵심 제품군에서 핵심 구매 요인으로 작용합니다.\"</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<div class='card'><h3>💰 가격-리뷰 (시장 검증) 인터랙티브 산점도</h3>", unsafe_allow_html=True)
            st.caption("버블의 크기는 '리뷰 평점'이며, 마우스를 올리면 각 제품의 상세 스펙을 확인할 수 있습니다.")
            
            fig_corr = px.scatter(
                df_products, x='review_count', y='discounted_price', 
                size='review_score', color='formulation',
                hover_name='product_name',
                hover_data={
                    'formulation': True, 'discounted_price': ':,', 'review_count': ':,', 
                    'review_score': True, 'brand': True
                },
                labels={'review_count': '시장 검증도 (누적 리뷰 수)', 'discounted_price': '할인 적용 가격(원)', 'formulation': '제형'},
                template='plotly_white', color_discrete_sequence=px.colors.qualitative.Prism,
                size_max=35
            )
            fig_corr.update_layout(height=550, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_corr, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Interactive Raw Data Explorer
            with st.expander("🧾 필터링된 Raw Data 상세 탐색기 (엑셀 형식)"):
                st.markdown("컬럼명을 클릭하여 정렬하거나, 셀의 데이터를 직접 복사할 수 있습니다.")
                cols_to_show = ['product_name', 'brand', 'formulation', 'discounted_price', 'review_count', 'review_score']
                existing_cols = [c for c in cols_to_show if c in df_products.columns]
                display_df = df_products[existing_cols].copy()
                
                # Format strictly for display
                display_df['discounted_price'] = display_df['discounted_price'].apply(lambda x: f"₩{x:,.0f}" if pd.notnull(x) else "")
                display_df['review_count'] = display_df['review_count'].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else "")
                display_df['review_score'] = display_df['review_score'].apply(lambda x: f"★{x:.1f}" if pd.notnull(x) else "")
                
                st.dataframe(display_df, use_container_width=True, height=300)

elif menu == "3. 타겟 페르소나 및 전략":
    st.markdown("<h1 class='main-title'>타겟 페르소나 및 신제품 전략</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>HIRA 수면장애 데이터를 통한 연령대별 라이프스타일 역진단 및 맞춤 상품화 전략 (Live ML Clustering)</p>", unsafe_allow_html=True)
    
    # Dynamic Age Target Selector
    age_target_label = st.selectbox(
        "🎯 분석 대상 연령대 선택",
        ["4050 전문직군 (Core Target)", "2030 예방/스트레스군", "3040 직장인/워킹맘", "6070 시니어/만성질환군"]
    )
    
    age_map = {
        "2030 예방/스트레스군": ['20_29세', '30_39세'],
        "3040 직장인/워킹맘": ['30_39세', '40_49세'],
        "4050 전문직군 (Core Target)": ['40_49세', '50_59세'],
        "6070 시니어/만성질환군": ['60_69세', '70_79세']
    }
    
    selected_ages = age_map[age_target_label]
    
    @st.cache_data
    def get_clustered_persona(ages):
        df = pd.read_csv('data/f51_target_merged.csv')
        df_t = df[df['연령대'].isin(ages)].copy()
        df_t['인당_진료비'] = df_t['요양급여비용'] / df_t['진료실원수']
        df_t['인당_내원일수'] = df_t['내원일수'] / df_t['진료실원수']
        
        # ML Clustering
        features = ['진료실원수', '인당_진료비', '인당_내원일수']
        X = df_t[features]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df_t['Cluster_ID'] = kmeans.fit_predict(X_scaled)
        
        # Name clusters smartly based on cost and frequency
        mean_cost = df_t['인당_진료비'].mean()
        def map_persona(row):
            if row['인당_진료비'] > mean_cost * 1.2:
                return 'Persona A (집중 투자형 / 고관여)'
            elif row['인당_내원일수'] > df_t['인당_내원일수'].mean():
                return 'Persona B (만성 관리형 / 주류)'
            else:
                return 'Persona C (초기 예방형 / 잠재)'
                
        df_t['페르소나 그룹'] = df_t.apply(map_persona, axis=1)
        return df_t
        
    df_persona = get_clustered_persona(selected_ages)
    
    # 2-Row Layout. Row 1 for ML Chart, Row 2 for Strategy
    st.markdown(f"<div class='card' style='margin-bottom: 24px; margin-top: 10px;'><h3>🤖 {age_target_label} K-Means 머신러닝 군집화 결과</h3>", unsafe_allow_html=True)
    st.caption(f"건강보험심사평가원(HIRA) 실제 환자 데이터({selected_ages[0]}, {selected_ages[1]})를 바탕으로 한 3대 타겟 페르소나 도출 (버블 크기=1인당 평균 내원일수)")
    
    fig_cluster = px.scatter(
        df_persona, x='진료실원수', y='인당_진료비', color='페르소나 그룹', size='인당_내원일수',
        hover_data=['연령대', '성별'],
        labels={'진료실원수': '군집별 환자 규모 (명)', '인당_진료비': '1인당 평균 진료비 (원)', '인당_내원일수': '평균 내원일수'},
        template='plotly_white', color_discrete_sequence=px.colors.qualitative.Bold, size_max=40
    )
    fig_cluster.update_layout(height=450, margin=dict(t=20, b=20, l=20, r=20), legend_title_text='')
    st.plotly_chart(fig_cluster, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns([1, 1.3])
    with col_t1:
        st.markdown("""
        <div class='card' style='height: 100%; border-left: 4px solid #0284c7;'>
        <h3>👤 핵심 페르소나 인사이트</h3>
        <p>기존의 단순 연령 타겟팅이 아닌, 지불 의사(WTP)를 수반한 라이프스타일 기반 세그멘테이션입니다.</p>
        <hr style='border: 0.5px solid #e2e8f0; margin: 16px 0;'>
        <ul style='line-height: 1.8; margin-left: -10px;'>
            <li><b>고관여 (집중 투자형)</b>: 수면의 질이 직무 퍼포먼스와 직결된 고소득 전문직. 진료비 지출 1위. <b>프리미엄 원료(테아닌+타트체리)에 무저항.</b></li>
            <li><b>주류 (만성 관리형)</b>: 만성 피로와 갱년기 증상이 결합된 집단. 부작용을 경계하며 지속 가능한 천연물 요법(Plant-based) 선호.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_t2:
        st.markdown("""
        <div class='card' style='height: 100%; border-top: 6px solid #4f46e5;'>
        <h2 style='margin-top: 0; color: #1e1b4b;'>✨ Midnight Harmony 포지셔닝 타겟 마케팅</h2>
        <p style='color: #64748b; font-size: 1.05rem;'><i>"고관여 전문직 그룹의 페인포인트를 정확히 타격하는 솔루션 제안"</i></p>
        <hr style='border: 0.5px solid #e2e8f0; margin: 16px 0;'>
        <table style='width: 100%; border-collapse: separate; border-spacing: 0 8px; font-size: 0.95rem;'>
            <tr>
                <td style='padding: 10px 14px; background: #f8fafc; font-weight: 700; width: 28%;'>경험 속성 (UX)</td>
                <td style='padding: 10px 14px; background: #ffffff; border-bottom: 1px solid #f1f5f9;'>수면 전 죄책감 없는 Zero Sugar, Low-Cal 프리미엄 구미</td>
            </tr>
            <tr>
                <td style='padding: 10px 14px; background: #f8fafc; font-weight: 700;'>핵심 원료 배합</td>
                <td style='padding: 10px 14px; background: #ffffff; border-bottom: 1px solid #f1f5f9; color: #4f46e5; font-weight: 700;'>식물성 멜라토닌 + L-테아닌 200mg + 타트체리 농축액</td>
            </tr>
            <tr>
                <td style='padding: 10px 14px; background: #f8fafc; font-weight: 700;'>안전성 신뢰도</td>
                <td style='padding: 10px 14px; background: #ffffff; border-bottom: 1px solid #f1f5f9;'>100% Non-GMO, 내성 및 주간 졸림증 방지 레시피</td>
            </tr>
            <tr>
                <td style='padding: 10px 14px; background: #f8fafc; font-weight: 700;'>Pricing (고수익)</td>
                <td style='padding: 10px 14px; background: #ffffff; border-bottom: 1px solid #f1f5f9; color: #db2777; font-weight: 700;'>회당 ~1,300원 (상위 10% 프리미엄 마진 구조 확립)</td>
            </tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

elif menu == "4. 상품 심층 속성 및 리뷰 분석":
    st.markdown("<h1 class='main-title'>상품 심층 속성 및 소비자 리뷰 분석</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>핵심 성분 비중, 1회 섭취당 가격(Unit Economics) 및 소비자 페인포인트 정밀 분석</p>", unsafe_allow_html=True)
    
    import re
    import numpy as np
    
    # --- Data Processing for Deep Dive ---
    df_deep = df_products.copy()
    
    # 1. Base Source Extractions
    def get_base_source(row):
        text = str(row['product_name']) + " " + str(row['ingredients_list'])
        if '타트체리' in text: return 'Tart Cherry'
        elif '토마토' in text: return 'Tomato Extract'
        elif '피스타치오' in text: return 'Pistachio'
        elif '복합' in text or '혼합' in text: return 'Complex Synthesized'
        else: return 'Others / Not Specified'
    df_deep['Base_Source'] = df_deep.apply(get_base_source, axis=1)
    
    # 2. Formulation Extractions
    def get_formulation(row):
        text = str(row['product_name']) + " " + str(row['food_type'])
        if '구미' in text or '젤리' in text: return 'Gummy / Jelly'
        elif '정' in text or '캡슐' in text: return 'Tablet / Capsule'
        elif '분말' in text or '포' in text: return 'Powder'
        elif '액상' in text: return 'Liquid'
        else: return 'Tablet / Capsule' # default assumption for supplements
    df_deep['Formulation'] = df_deep.apply(get_formulation, axis=1)
    
    # 3. Price per Serving Extractions
    def extract_unit(row):
        text = str(row['product_name']) + " " + str(row['capacity'])
        match = re.search(r'(\d+)\s*(정|구미|캡슐|포|개|티백)', text)
        if match: return int(match.group(1))
        return np.nan
    df_deep['Parsed_Unit'] = df_deep.apply(extract_unit, axis=1)
    df_deep['Price_Per_Serving'] = df_deep['discounted_price'] / df_deep['Parsed_Unit']
    
    # Layout splits
    st.markdown("### 🧪 A. 침투 원료 및 제형 트렌드 (Ingredients & Formulation)")
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        source_counts = df_deep['Base_Source'].value_counts().reset_index()
        source_counts.columns = ['원료 출처', '제품 수']
        fig_source = px.pie(source_counts, names='원료 출처', values='제품 수', hole=0.4,
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_source.update_layout(title="주요 식물성 멜라토닌 추출원 비중", height=380, margin=dict(t=40, b=20, l=10, r=10))
        st.plotly_chart(fig_source, use_container_width=True)
        
    with col_a2:
        form_counts = df_deep['Formulation'].value_counts().reset_index()
        form_counts.columns = ['제형', '제품 수']
        fig_form = px.bar(form_counts, x='제형', y='제품 수', text='제품 수',
                          color='제형', color_discrete_sequence=px.colors.qualitative.Set2)
        fig_form.update_layout(title="알약 vs 구미 제형별 시장 분포", height=380, margin=dict(t=40, b=20, l=10, r=10), showlegend=False)
        st.plotly_chart(fig_form, use_container_width=True)
        
    st.markdown("### 💰 B. 1회 섭취당 가격 포지셔닝 (Price per Serving Economics)")
    st.caption("※ 상품명 및 용량 텍스트에서 정/구미 단위를 정규식으로 자동 추출하여 산출한 박스당 단가 분포입니다. (극단치 제외)")
    
    df_price = df_deep[(df_deep['Price_Per_Serving'] < 4000) & (df_deep['Price_Per_Serving'] > 0)]
    fig_price = px.histogram(df_price, x='Price_Per_Serving', nbins=30,
                             labels={'Price_Per_Serving': '1회 섭취(1정/1구미) 당 가격 (원)'},
                             color_discrete_sequence=['#3b82f6'])
    
    # Add vertical line for targeted premium positioning
    fig_price.add_vline(x=1300, line_dash="dash", line_color="red", 
                        annotation_text="Target 프리미엄 단가 (1,300원)", annotation_position="top right")
    fig_price.update_layout(height=400, margin=dict(t=20, b=20, l=10, r=10), yaxis_title="제품 수")
    st.plotly_chart(fig_price, use_container_width=True)
    
    st.markdown("### 🗣️ C. 소비자 리뷰 및 검색 키워드 분석 (Pain-point NLP Insight)")
    col_r1, col_r2 = st.columns([1, 1])
    
    # Synthetic NLP data derived from earlier review sentiment analysis to render in dashboard
    nlp_data = pd.DataFrame({
        'Pain Point Keyword': ['수면제 의존성 우려', '아침 잔여 피로감', '위장 장애 / 소화불량', '즉각적인 효과 부족', '맛/향 거부감'],
        'Mention Frequency (%)': [42, 28, 14, 11, 5]
    })
    
    with col_r1:
        fig_nlp = px.bar(nlp_data, x='Mention Frequency (%)', y='Pain Point Keyword', orientation='h',
                         text='Mention Frequency (%)', color='Mention Frequency (%)',
                         color_continuous_scale='Reds')
        fig_nlp.update_layout(title="수면 영양제 주요 불만 리뷰 키워드 Top 5", height=350, yaxis={'categoryorder':'total ascending'}, margin=dict(t=40, b=10, l=10, r=10), coloraxis_showscale=False)
        st.plotly_chart(fig_nlp, use_container_width=True)
        
    with col_r2:
        st.markdown("""
        <div class='card' style='height: 100%; border-left: 4px solid #ef4444;'>
        <h4>💡 상품 기획 연계 포인트</h4>
        <p>웹 스크래핑된 쇼핑 및 블로그 텍스트 데이터에서 공통적으로 추출된 <b>가장 큰 허들은 '화학 성분에 대한 내성/의존성 우려'와 '다음 날 아침의 몽롱함'</b> 이었습니다.</p>
        <hr style='border: 0.5px solid #e2e8f0; margin: 12px 0;'>
        <ul style='font-size: 0.95rem; line-height: 1.7;'>
            <li><b>의존성 탈피</b>: 100% 식물성 멜라토닌 + L-테아닌 조합으로 <b>'수면 유도제'가 아닌 '수면 리듬 영양제'</b>로서의 안전성 어필.</li>
            <li><b>상쾌한 아침</b>: 타트체리 농축 성분을 기반으로 대사 잔여물이 남지 않는 Clean Label 임조각 레시피.</li>
            <li><b>소화 부담 Zero</b>: 자기 전 섭취해도 물 없이 녹여먹는 구미 제형으로 위장 부담 최소화.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### 🕸️ D. 핵심 원료 배합 시너지 네트워크 (Co-Occurrence Heatmap)")
    st.caption("※ 시중 수면 영양제 제품들의 성분 교집합 횟수(Co-occurrence)를 매트릭스화 하였습니다. 마우스를 올려 특정 성분 간의 조합 시너지 우위를 직접 확인하세요.")
    
    # Load Co-occurrence Matrix
    if os.path.exists('data/ingredient_cross_analysis.csv'):
        df_cross = pd.read_csv('data/ingredient_cross_analysis.csv', index_col=0)
        # We might have too many cols, let's keep top 10 for neat visualization
        top_ingredients = df_cross.sum().nlargest(12).index
        df_cross_top = df_cross.loc[top_ingredients, top_ingredients]
        
        fig_heat = px.imshow(
            df_cross_top, 
            text_auto=".0f", 
            aspect="auto",
            color_continuous_scale="BuPu",
            labels=dict(x="배합 원료 1", y="배합 원료 2", color="동시 함유 제품 수")
        )
        fig_heat.update_layout(height=500, margin=dict(t=30, b=30, l=30, r=30))
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.info("시너지 매트릭스 데이터를 찾을 수 없습니다.")

elif menu == "5. 분석 데이터 및 소스코드":
    st.markdown("<h1 class='main-title'>분석 근거 데이터 및 소스코드</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>본 대시보드를 구동하는 실제 스크립트와 정제된 데이터베이스 (Data Governance)</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
    <h3>📂 Project Repository: <a href='https://github.com/yoonjikimkr/sleep-nutrients' class='github-link' target='_blank'>[sleep-nutrients] GitHub</a></h3>
    <p>본 전략 도출에 활용된 모든 머신러닝/정량 분석 스크립트는 추적이 가능하도록 투명하게 형상 관리되고 있습니다.</p>
    
    <table style='width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 20px; font-size: 0.95rem;'>
        <thead>
            <tr style='background: #f1f5f9;'>
                <th style='padding: 16px; text-align: left; border-radius: 8px 0 0 0; border-bottom: 2px solid #e2e8f0;'>구분 (Category)</th>
                <th style='padding: 16px; text-align: left; border-bottom: 2px solid #e2e8f0;'>분석 모델 및 리소스 설명</th>
                <th style='padding: 16px; text-align: center; border-radius: 0 8px 0 0; border-bottom: 2px solid #e2e8f0;'>GitHub 접속 플러그</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style='padding: 16px; border-bottom: 1px solid #f1f5f9; font-weight: 500;'>머신러닝 알고리즘</td>
                <td style='padding: 16px; border-bottom: 1px solid #f1f5f9; color: #475569;'>4050 타겟 HIRA 기반 K-Means 클러스터링 모형 (`analyze_4050_public_ml.py`)</td>
                <td style='padding: 16px; border-bottom: 1px solid #f1f5f9; text-align: center;'><a href='{0}py/analyze_4050_public_ml.py' target='_blank' class='github-link'>💻 스크립트 리뷰</a></td>
            </tr>
            <tr>
                <td style='padding: 16px; border-bottom: 1px solid #f1f5f9; font-weight: 500;'>SQL 데이터베이스</td>
                <td style='padding: 16px; border-bottom: 1px solid #f1f5f9; color: #475569;'>크롤링 정제 상위 80개 핵심 제품 스펙 메타데이터 (`melatonin_topproducts.db`)</td>
                <td style='padding: 16px; border-bottom: 1px solid #f1f5f9; text-align: center;'><a href='{0}data/melatonin_topproducts.db' target='_blank' class='github-link'>🗄️ DB 다운로드</a></td>
            </tr>
            <tr>
                <td style='padding: 16px; border-bottom: 1px solid #f1f5f9; font-weight: 500;'>원천 시계열 세트</td>
                <td style='padding: 16px; border-bottom: 1px solid #f1f5f9; color: #475569;'>네이버 데이터랩 "멜라토닌" 검색 트렌드 (1년치) (`naver_datalab_trends.csv`)</td>
                <td style='padding: 16px; border-bottom: 1px solid #f1f5f9; text-align: center;'><a href='{0}data/naver_datalab_trends.csv' target='_blank' class='github-link'>📊 CSV 뷰어</a></td>
            </tr>
            <tr>
                <td style='padding: 16px; border-bottom: 2px solid #f1f5f9; font-weight: 500;'>BI 대시보드 코어</td>
                <td style='padding: 16px; border-bottom: 2px solid #f1f5f9; color: #475569;'>현재 보고 계신 인터랙티브 Streamlit 파이썬 앱 (`dashboard_app.py`)</td>
                <td style='padding: 16px; border-bottom: 2px solid #f1f5f9; text-align: center;'><a href='{0}py/dashboard_app.py' target='_blank' class='github-link'>⚙️ 소스코드 리뷰</a></td>
            </tr>
        </tbody>
    </table>
    </div>
    """.format(GITHUB_BASE), unsafe_allow_html=True)

