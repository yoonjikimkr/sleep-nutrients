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
    ["1. 시장 개요 및 트렌드", "2. 데이터 기반 시장 분석", "3. 타겟 페르소나 및 전략", "4. 분석 데이터 및 소스코드"]
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
    st.markdown("<p class='sub-title'>HIRA 수면장애 데이터를 통한 '4050 전문직군' 라이프스타일 역진단 및 맞춤 상품화 전략</p>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns([1, 1.4])
    
    with col_t1:
        st.markdown("""
        <div class='card' style='height: 100%;'>
        <h3>👤 핵심 타겟: 4050 전문직군 (Professional)</h3>
        <p>사회적 책임이 가장 큰 연령층이며, 생물학적인 멜라토닌 분비 저하와 직무 스트레스가 결합된 <b>시장 내 가장 높은 지불 의사(WTP)를 가진 고객층</b>입니다.</p>
        <hr style='border: 0.5px solid #e2e8f0; margin: 20px 0;'>
        <ul style='line-height: 1.8;'>
            <li><b>Persona A (High Value)</b>: 고가 시너지 성분에 매우 민감하며 즉각적이고 부작용 없는 효과를 기대함.</li>
            <li><b>Persona B (Continuous)</b>: 갱년기 및 만성 피로 관리를 위한 정기 구독형 라이프스타일 추구.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if os.path.exists('data/chart_4050_persona_clusters.png'):
            st.image('data/chart_4050_persona_clusters.png', caption='HIRA 데이터 기반 K-Means 클러스터 분포도', use_container_width=True)
        
    with col_t2:
        st.markdown("""
        <div class='card' style='border-top: 8px solid #4f46e5; height: 100%;'>
        <h2 style='margin-top: 0; color: #1e1b4b;'>✨ 전략 제안: Midnight Harmony</h2>
        <p style='color: #64748b; font-size: 1.1rem;'><i>"전문가를 위한 단 하나의 프리미엄 식물성 멜라토닌 솔루션"</i></p>
        <hr style='border: 0.5px solid #e2e8f0; margin: 20px 0;'>
        <table style='width: 100%; border-collapse: separate; border-spacing: 0 12px; font-size: 1rem;'>
            <tr>
                <td style='padding: 12px 16px; background: #f8fafc; border-radius: 8px 0 0 8px; font-weight: 700; width: 30%;'>Formulation (제형)</td>
                <td style='padding: 12px 16px; background: #ffffff; border: 1px solid #f1f5f9; border-left: none; border-radius: 0 8px 8px 0;'>맛있는 프리미엄 구미 (Zero Sugar / Low Calorie)</td>
            </tr>
            <tr>
                <td style='padding: 12px 16px; background: #f8fafc; border-radius: 8px 0 0 8px; font-weight: 700;'>Ingredient (원료)</td>
                <td style='padding: 12px 16px; background: #ffffff; border: 1px solid #f1f5f9; border-left: none; border-radius: 0 8px 8px 0;'>Tart Cherry + Theanine 200mg + Tryptophan 시너지</td>
            </tr>
            <tr>
                <td style='padding: 12px 16px; background: #f8fafc; border-radius: 8px 0 0 8px; font-weight: 700;'>Safety (안전성)</td>
                <td style='padding: 12px 16px; background: #ffffff; border: 1px solid #f1f5f9; border-left: none; border-radius: 0 8px 8px 0;'>1.5mg Mild Content / 100% Non-GMO 인증</td>
            </tr>
            <tr>
                <td style='padding: 12px 16px; background: #f8fafc; border-radius: 8px 0 0 8px; font-weight: 700;'>Price (가격 정책)</td>
                <td style='padding: 12px 16px; background: #ffffff; border: 1px solid #f1f5f9; border-left: none; border-radius: 0 8px 8px 0; color: #db2777; font-weight: 700;'>~1,300원/회 (시장 상위 10% 티어 타겟)</td>
            </tr>
            <tr>
                <td style='padding: 12px 16px; background: #f8fafc; border-radius: 8px 0 0 8px; font-weight: 700;'>Channel (유통망)</td>
                <td style='padding: 12px 16px; background: #ffffff; border: 1px solid #f1f5f9; border-left: none; border-radius: 0 8px 8px 0;'>SSG/백화점 (신뢰 확보) &rarr; Naver/GMarket (볼륨 확장)</td>
            </tr>
        </table>
        
        <div class='script-box' style='margin-top: 24px;'>
            "미드나잇 하모니는 자기 전 물 없이도 부담 없이 먹을 수 있는 무설탕 구미 제형에, 테아닌 200mg의 강력한 릴렉세이션 효과를 결합하여 수면 질 저하로 고통받는 4050 프로페셔널의 수면 사이클을 근본적으로 개선합니다."
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div style='background: white; border: 1px dashed #cbd5e1; border-radius: 12px; padding: 20px; text-align: center; margin-top: 10px;'>
        <h4 style='color: #475569; margin-top: 0;'>📝 팀 논의 / 피드백 메모</h4>
        <p style='color: #94a3b8; font-size: 0.9rem;'>추후 라이브 프레젠테이션 시, 이 공간에 예상 매출 시뮬레이터(What-If Calculator) 또는 실시간 피드백 폼을 추가하여 경영진과 인터랙티브하게 소통할 수 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)

elif menu == "4. 분석 데이터 및 소스코드":
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

