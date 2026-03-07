import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import numpy as np
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="Sleep Insights: Surge & Stats",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    h1, h2, h3 { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_all_data():
    data_dir = "data"
    
    # 트렌드 데이터 로드
    with open(os.path.join(data_dir, "search_trend_past.json"), "r", encoding="utf-8") as f:
        past_json = json.load(f)
    with open(os.path.join(data_dir, "search_trend_present.json"), "r", encoding="utf-8") as f:
        present_json = json.load(f)
        
    keywords = ["불면", "잠이 안 와", "수면 영양제", "멜라토닌"]
    blog_dfs = {}
    shop_dfs = {}
    for kw in keywords:
        bp, sp = os.path.join(data_dir, f"blog_{kw}.csv"), os.path.join(data_dir, f"shop_{kw}.csv")
        if os.path.exists(bp): blog_dfs[kw] = pd.read_csv(bp)
        if os.path.exists(sp): shop_dfs[kw] = pd.read_csv(sp)
            
    return past_json, present_json, blog_dfs, shop_dfs

def detect_surges(df, window=7, threshold=2.0):
    """
    급증 시점 탐지 로직:
    7일 이동 평균(Rolling Mean)이 이전 30일 평균 대비 일정 배수(threshold) 이상 높을 때 급증 시작으로 간주
    """
    df = df.sort_values('period').copy()
    df['rolling_mean'] = df['ratio'].rolling(window=window).mean()
    df['baseline'] = df['ratio'].rolling(window=30).mean().shift(1)
    
    # 급증 조건: 현재 이동 평균 > (이전 베이스라인 * threshold) AND 현재 비율이 유의미(예: > 5)
    df['is_surge'] = (df['rolling_mean'] > df['baseline'] * threshold) & (df['ratio'] > 5)
    
    # 연속된 급증 구간 중 첫 번째 지점만 추출
    df['surge_start'] = df['is_surge'] & (~df['is_surge'].shift(1).fillna(False))
    return df[df['surge_start']]

def main():
    st.title("🌙 Sleep Insights Analytics (Surge & Deep Stats)")
    st.markdown("과거와 현재의 검색 변화 및 급증(Surge) 모멘텀 분석")

    try:
        past_json, present_json, blog_dfs, shop_dfs = load_all_data()
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return

    st.sidebar.title("⚙️ 분석 필터")
    selected_keywords = st.sidebar.multiselect(
        "분석 키워드", ["불면", "잠이 안 와", "수면 영양제", "멜라토닌"], default=["불면", "멜라토닌"]
    )
    
    # Surge 탐지 민감도 조절
    surge_sensitivity = st.sidebar.slider("급증 탐지 민감도 (배수)", 1.5, 5.0, 2.5, 0.1)

    if not selected_keywords:
        st.warning("분석할 키워드를 선택해 주세요.")
        return

    tab1, tab2, tab3 = st.tabs(["🔥 급증 & 통합 트렌드", "🕰️ 과거 vs 현재 비교", "💬 콘텐츠 및 통계"])

    # 데이터 가공 (공통)
    def process_trend(json_data, label):
        frames = []
        for res in json_data['results']:
            if res['title'] in selected_keywords:
                df = pd.DataFrame(res['data'])
                df['keyword'] = res['title']
                df['period_group'] = label
                frames.append(df)
        return pd.concat(frames) if frames else pd.DataFrame()

    df_past = process_trend(past_json, "과거")
    df_present = process_trend(present_json, "현재")
    df_all = pd.concat([df_past, df_present]).copy()
    df_all['period'] = pd.to_datetime(df_all['period'])
    df_all = df_all.sort_values(['keyword', 'period'])

    # --- Tab 1: 급증 & 통합 트렌드 ---
    with tab1:
        st.subheader("🔥 검색량 급증(Surge) 시점 탐지")
        st.markdown(f"전체 기간 중 검색량이 이전 평균 대비 **{surge_sensitivity}배** 이상 급증한 지점을 분석합니다.")
        
        all_surges = []
        fig_surge = go.Figure()

        for kw in selected_keywords:
            df_kw = df_all[df_all['keyword'] == kw].copy()
            # 차트 베이스 라인 추가
            fig_surge.add_trace(go.Scatter(x=df_kw['period'], y=df_kw['ratio'], name=kw, mode='lines', opacity=0.6))
            
            # 급증 탐지
            surges = detect_surges(df_kw, threshold=surge_sensitivity)
            if not surges.empty:
                all_surges.append(surges)
                # 어노테이션(주석) 및 마커 추가
                fig_surge.add_trace(go.Scatter(
                    x=surges['period'], y=surges['ratio'], 
                    mode='markers', name=f"{kw} 급증",
                    marker=dict(size=10, symbol='triangle-up', line=dict(width=2))
                ))
                
        fig_surge.update_layout(
            title="통합 검색 트렌드 및 급증 시점 (Annotations)",
            template="plotly_dark",
            xaxis_title="기간",
            yaxis_title="검색 비율 (상대치)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_surge, use_container_width=True)

        # 급증 시점 리스트
        if all_surges:
            st.markdown("### 📍 포착된 급증 모멘텀 리스트")
            df_surge_list = pd.concat(all_surges)[['keyword', 'period', 'ratio']].sort_values('period', ascending=False)
            df_surge_list.columns = ['키워드', '급증 발생일', '당시 검색 비율']
            st.dataframe(df_surge_list, use_container_width=True)
        else:
            st.info("현재 설정된 민감도에서는 급증 지점이 발견되지 않았습니다.")

    # --- Tab 2: 과거 vs 현재 비교 ---
    with tab2:
        st.subheader("🕰️ 시기별 관심도 대조")
        avg_compare = df_all.groupby(['period_group', 'keyword'])['ratio'].mean().reset_index()
        fig_bar = px.bar(avg_compare, x='keyword', y='ratio', color='period_group', barmode='group',
                        title="과거(2016-2020) vs 현재(2021-2026) 평균 검색 강도", template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- Tab 3: 콘텐츠 및 통계 ---
    with tab3:
        st.subheader("📊 키워드별 심층 통계 요약")
        
        # 심층 통계 계산
        stats_list = []
        for kw in selected_keywords:
            df_kw = df_all[df_all['keyword'] == kw]
            mean_val = df_kw['ratio'].mean()
            std_val = df_kw['ratio'].std()
            cv = (std_val / mean_val * 100) if mean_val > 0 else 0 # 변동계수
            max_val = df_kw['ratio'].max()
            current_val = df_kw.iloc[-1]['ratio'] if not df_kw.empty else 0
            
            stats_list.append({
                "키워드": kw,
                "평균": mean_val,
                "표준편차": std_val,
                "변동계수(CV, %)": cv,
                "최고치(Peak)": max_val,
                "현재 상태(Ratio)": current_val,
                "활성 지수(최고대비 현재)": (current_val / max_val * 100) if max_val > 0 else 0
            })
        
        st.dataframe(pd.DataFrame(stats_list).style.format(precision=2), use_container_width=True)
        st.markdown("""
            - **변동계수(CV)**: 값이 클수록 검색량의 기복이 심함(이슈성 강함).
            - **활성 지수**: 역대 최고 관심도 대비 현재 어느 정도 수준인지를 나타냄.
        """)

        st.divider()
        st.subheader("💬 블로그/쇼핑 매칭 데이터")
        for kw in selected_keywords:
            with st.expander(f"🔍 {kw} 실시간 데이터"):
                it1, it2 = st.columns(2)
                if kw in blog_dfs:
                    with it1: st.markdown("##### 최신 블로그 인사이트"); st.dataframe(blog_dfs[kw][['title', 'postdate']].head(5))
                if kw in shop_dfs:
                    with it2: st.markdown("##### 쇼핑 인기 상품"); st.dataframe(shop_dfs[kw][['title', 'lprice']].head(5))

if __name__ == "__main__":
    main()
