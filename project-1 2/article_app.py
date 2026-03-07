import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="Sleep News Insights",
    page_icon="📰",
    layout="wide"
)

# 데이터 로드 함수
@st.cache_data
def load_data():
    base_dir = "/Users/juns/Desktop/fcicb7/project-1/articles"
    files = {
        "불면 증가": "articles_불면_증가.csv",
        "멜라토닌 부작용": "articles_멜라토닌_부작용.csv",
        "수면제 의존": "articles_수면제_의존.csv"
    }
    
    data_dict = {}
    for label, filename in files.items():
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            df = pd.read_csv(path)
            # Naver pubDate format: "Sat, 07 Feb 2026 14:00:00 +0900"
            df['date'] = pd.to_datetime(df['pubDate'], errors='coerce')
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.to_period('M').astype(str)
            df['text'] = df['title'].fillna('') + ' ' + df['description'].fillna('')
            data_dict[label] = df
            
    return data_dict

data = load_data()

st.title("📰 뉴스 기사 기반 수면 이슈 분석 대시보드")
st.markdown("수집된 뉴스 데이터를 바탕으로 수면 관련 사회적 트렌드와 사용자 우려 사항을 분석합니다.")

if not data:
    st.error("데이터 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
else:
    tabs = st.tabs(["📊 보도 트렌드", "⚠️ 멜라토닌 부정 이슈", "🌿 대체 성분 추이", "📄 원본 데이터"])

    # 1. 월별 기사수 line chart
    with tabs[0]:
        st.subheader("1. 월별 기사 발행 추이 (불면 증가 vs 멜라토닌 부작용)")
        
        df_bul = data.get("불면 증가", pd.DataFrame())
        df_mel = data.get("멜라토닌 부작용", pd.DataFrame())
        
        if not df_bul.empty and not df_mel.empty:
            count_bul = df_bul.groupby('month').size().reset_index(name='count')
            count_bul['keyword'] = '불면 증가'
            
            count_mel = df_mel.groupby('month').size().reset_index(name='count')
            count_mel['keyword'] = '멜라토닌 부작용'
            
            combined = pd.concat([count_bul, count_mel])
            
            fig = px.line(combined, x='month', y='count', color='keyword',
                          markers=True, title="월별 기사 발행 건수 비교",
                          labels={'month': '연월', 'count': '기사 수'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("분석할 기사 데이터가 부족합니다.")

    # 2. 멜라토닌 부정 키워드 비율 (바차트)
    with tabs[1]:
        st.subheader("2. 멜라토닌 부정 이슈 분석 (년도별 부정 기사 비율)")
        df_mel = data.get("멜라토닌 부작용", pd.DataFrame())
        
        if not df_mel.empty:
            neg_keywords = ["부작용", "의존", "내성", "중독", "위험", "경고", "과다복용", "우울", "두통"]
            
            def has_neg(text):
                return any(kw in text for kw in neg_keywords)
            
            df_mel['is_negative'] = df_mel['text'].apply(has_neg)
            
            # 년도별 비율 계산
            annual_neg = df_mel.groupby('year').apply(
                lambda x: (x['is_negative'].sum() / len(x)) * 100
            ).reset_index(name='ratio')
            
            fig = px.bar(annual_neg, x='year', y='ratio', 
                         title="년도별 멜라토닌 부정 키워드 언급 기사 비율 (%)",
                         labels={'year': '년도', 'ratio': '부정 기사 비율 (%)'},
                         color_discrete_sequence=['#E74C3C'])
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"**분석 키워드**: {', '.join(neg_keywords)}")
        else:
            st.warning("멜라토닌 부작용 기사 데이터가 없습니다.")

    # 3. 대체 성분 추이
    with tabs[2]:
        st.subheader("3. 대체 성분 및 비호르몬 수면 보조 키워드 언급 추이")
        df_mel = data.get("멜라토닌 부작용", pd.DataFrame())
        
        if not df_mel.empty:
            alt_keywords = ["마그네슘", "테아닌", "GABA", "감태", "락티움", "비호르몬", "자연유래", "대체"]
            
            # 각 키워드별 년도별 빈도 계산
            alt_trends = []
            for kw in alt_keywords:
                temp = df_mel[df_mel['text'].str.contains(kw, na=False)].groupby('year').size().reset_index(name='count')
                temp['ingredient'] = kw
                alt_trends.append(temp)
            
            alt_df = pd.concat(alt_trends)
            
            fig = px.area(alt_df, x='year', y='count', color='ingredient',
                          title="년도별 보조 성분 언급 빈도 추이",
                          labels={'year': '년도', 'count': '언급 횟수'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("데이터가 없습니다.")

    # 4. 원본 데이터
    with tabs[3]:
        st.subheader("데이터 상세 보기")
        target_kw = st.selectbox("키워드 선택", list(data.keys()))
        st.dataframe(data[target_kw][['date', 'title', 'description', 'originallink']], use_container_width=True)
