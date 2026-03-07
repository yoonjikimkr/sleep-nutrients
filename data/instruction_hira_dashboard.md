# HIRA 수면 장애 대시보드 구축 지시서 (instruction_hira_dashboard.md)

이 지시서는 정제된 `f51_target_merged.csv` 데이터를 활용하여 Streamlit 기반의 마케팅 분석 대시보드를 구축하기 위한 가이드를 제공합니다.

## 1. 개발 환경 및 라이브러리
- **Framework**: Streamlit
- **Visualization**: Plotly (Plotly Express 추천)
- **Data Handling**: Pandas

## 2. 데이터 데이터셋 사양
- **파일명**: `f51_target_merged.csv`
- **주요 컬럼**:
    - `상병코드`, `성별`, `연령대`, `연도` (Dimension)
    - `진료실원수`, `내원일수`, `처방일수`, `요양급여비용`, `본인부담금` (Measure)

---

## 3. 대시보드 레이아웃 및 기능

### 3.1 사이드바 (Sidebar) 필터
- **연도 선택**: 다중 선택(multiselect) 또는 단일 선택(selectbox). 기본값은 전체 또는 최신 연도.
- **성별 선택**: 라디오 버튼 또는 multiselect. ('남', '여' 필터링)

### 3.2 메인 화면 시각화 (5개 핵심 영역)

1. **핵심 타겟 파이 차트 (Pie Chart)**: 
    - 가장 높은 비율을 차지하는 **[연령대 + 성별]** 조합 시각화.
    - 지표: `진료실원수`.
2. **연령대별 진료 인원 (Stacked Bar Chart)**:
    - X축: `연령대`, Y축: `진료실원수`.
    - Color (Stack): `성별`.
3. **연도별 환자 증감 추이 (Line Chart)**:
    - X축: `연도`, Y축: `진료실원수`.
    - 성별 또는 연령대별 라인 구분 가능.
4. **Raw Data 요약 테이블 (Table)**:
    - 필터링된 결과의 상위 데이터 또는 요약 통계 테이블.
5. **성별 인원 비율 (Donut Chart)**:
    - 전체 환자 중 남/여 비율 시각화.

---

## 4. 구현 가이드라인 (Code Snippets)

### 데이터 로드 및 한글 설정
```python
import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv('f51_target_merged.csv')
```

### 시각화 예시 (Plotly)
```python
# 파이 차트
fig1 = px.pie(df_filtered, values='진료실원수', names='연령대', title='연령대별 환자 비율')

# 스택 바 차트
fig2 = px.bar(df_filtered, x='연령대', y='진료실원수', color='성별', barmode='stack')
```

---

## 5. 실행 및 확인
- 터미널에서 `streamlit run dashboard.py` 명령어로 실행.
- 웹 브라우저(localhost:8501)에서 필터 작동 및 차트 렌더링 확인.
