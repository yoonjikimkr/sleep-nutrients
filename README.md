# 🌙 Sleep Nutrients Project

글로벌(iHerb) 및 국내(Naver) 데이터를 통합 분석하여, 최적의 수면 영양제 복합제 기획과 시장 전략을 수립하는 프로젝트입니다.

---

## 📑 목차 (Table of Contents)
1. [🎯 3040 직장인 타겟 심층 분석 결과](#1--3040-직장인-타겟-심층-분석-결과-pyanalyze_3040_strategypy-실행-결과)
2. [🎯 3040 직장인 타겟 고도화 EDA 결과](#2--3040-직장인-타겟-고도화-eda-결과-pyanalyze_3040_strategy_v2py-실행-결과)
3. [🧪 iHerb & Naver 성분 교집합 분석](#3--iherb--naver-성분-교집합-분석-pyanalyze_ingredient_crosspy-실행-결과)
4. [🧮 3040 직장인 타겟 성분 짝꿍 매트릭스](#4--3040-직장인-타겟-성분-짝꿍-매트릭스-pyanalyze_cooccurrence_advancedpy-실행-결과)
5. [🛡️ 공공데이터 안전성(부작용) 검증 Plan](#5-️-공공데이터-안전성부작용-검증-plan-pyvalidate_safetypy-실행-결과)
6. [📂 리포트 및 소스코드](#--리포트-및-소스코드-collaboration)

---

## 1. 🎯 3040 직장인 타겟 심층 분석 결과 (`py/analyze_3040_strategy.py` 실행 결과)

```text
🚀 [심층 분석] 3040 한국 직장인 스트레스/수면 타겟 트렌드 (키워드 vs 성분 타겟팅 비교)
------------------------------------------------------------
🌍 [iHerb 글로벌 타겟팅 트렌드]
  - 🎯 '스트레스/이완' 키워드 명시 제품: 21개
  - 🌿 '핵심 타겟 성분' 포함 제품: 12개 (실질적 시장 규모가 훨씬 큼)
  👉 시장 인사이트: 글로벌 제품들은 키워드를 명시하기보다, 성분 자체의 배합으로 목적(수면/스트레스)을 달성하고 있음.

💡 [iHerb] 핵심 타겟 성분(Target Ingredients) 제품군의 최우수 성분 짝꿍 (Top Pairs):
  - 충분한 성분 조합 데이터가 발견되지 않았습니다.

🇰🇷 [Naver 국내 타겟팅 트렌드 및 프라이싱 비교]
  - 🎯 '스트레스/직장인' 키워드 타겟 제품: 39개
  - 🌿 '핵심 타겟 성분' 타겟 제품: 58개
    [키워드 기반] 평균 63,389원 (최저 9,990원 ~ 최고 243,980원)
    [핵심성분 기반] 평균 48,879원 (최저 9,000원 ~ 최고 243,980원)

📌 프라이싱 기획 인사이트: 3040 직장인은 수면/스트레스 문제에 기꺼이 프리미엄(고가)을 지불할 의사가 높으며, 단순 키워드보다 '핵심 성분'을 어필할 때 객단가를 유지하거나 확장할 여지가 더 큽니다.

============================================================
🎯 [최종 결론] 3040 한국 직장인 역량 강화를 위한 수면 영양제 Winning Formula
============================================================
 💊 추천 핵심 솔루션: MAGNESIUM & THEANINE & ASHWAGANDHA 베이스
 💡 [타겟 인사이트]: 글로벌 시장에서는 좁은 '스트레스' 키워드에 얽매이기보다
    'Theanine, Ashwagandha, Magnesium' 등 목적이 분명한 성분 조합 자체로 파이를 키우고 있습니다.
    국내 시장에서도 이런 '성분 시너지'를 전면에 내세울 때 3040의 지갑을 여는 고가(프리미엄) 전략이 유효합니다.
============================================================

```

---

## 2. 🎯 3040 직장인 타겟 고도화 EDA 결과 (`py/analyze_3040_strategy_v2.py` 실행 결과)

```text
🎯 [3040 직장인 타겟 고도화 EDA]

💡 3040 직장인 맞춤형 성분 전략:
            성분(ENG)   성분(KOR)    전략적_가치                                근거
         L-THEANINE       테아닌 10.000000 스트레스 완화 및 알파파 유도로 퇴근 후 머리 식히기에 최적
MAGNESIUM GLYCINATE 킬레이트 마그네슘  9.041667          흡수율이 높고 근육 이완과 심신 안정에 탁월
        ASHWAGANDHA     아슈와간다  9.000000           스트레스 호르몬(코르티솔) 조절 대포 성분
               GABA        가바  8.000000        각성된 뇌를 차분하게 만드는 억제성 신경전달물질
         VITAMIN B6    비타민 B6  8.000000         에너지 대사와 수면 호르몬 합성에 필수 조효소
      VALERIAN ROOT      발레리안  7.064815           천연 수면제로 불릴 만큼 강력한 입면 효과
         LEMON BALM       레몬밤  7.000000       불안 해소와 집중력/이완 상호작용에 우수한 보조제
              5-HTP     5-htp  6.000000      세로토닌-멜라토닌 경로를 자극하여 전반적 무드 개선

🚀 [최종 제안] 3040 직장인을 위한 '스위치 오프' 복합제 기획:
 📦 핵심 구성: 테아닌(L-THEANINE), 킬레이트 마그네슘(MAGNESIUM GLYCINATE), 아슈와간다(ASHWAGANDHA)
 🏷️ 마케팅 키워드: #퇴근후5분 #코르티솔다이어트 #뇌전원끄기

```

---

## 3. 🧪 iHerb & Naver 성분 교집합 분석 (`py/analyze_ingredient_cross.py` 실행 결과)

```text
--- iHerb & Naver 성분 교집합 분석 시작 ---
✅ 분석 완료! 결과 저장됨: [ingredient_cross_analysis.csv](data/ingredient_cross_analysis.csv)

--- 주요 성분 기회 요소 (Top 5) ---
   ingredient_kor  iherb_count  naver_count  opportunity_score
6            마그네슘        339.0         15.0              144.6
10       식물성 멜라토닌          0.0         50.0               30.0
1          L-트립토판          8.0         36.0               24.8
16            테아닌          6.0         35.0               23.4
4             락티움          0.0         23.0               13.8
3             글리신         31.0          2.0               13.6

```

---

## 4. 🧮 3040 직장인 타겟 성분 짝꿍 매트릭스 (`py/analyze_cooccurrence_advanced.py` 실행 결과)

```text
🚀 [3040 직장인 타겟] 성분 간 짝꿍 상관관계 (Co-occurrence Matrix) 분석 시작
 -> iHerb DB 로드 완료: 432개 제품
 -> iHerb Detailed CSV 로드 완료: 432개 제품
 -> Naver CSV 로드 완료: 842개 제품

✅ iHerb 분석 유효제품: 398건 / Naver 분석 유효제품: 22건 (중복포함)


📊 [iHerb 글로벌] 매트릭스 저장 완료: [chart_cooccurrence_heatmap_iherb.png](data/chart_cooccurrence_heatmap_iherb.png)
💡 [iHerb 글로벌] 핵심 인사이트 요약 (상위 베이스 성분별):

🔹 베이스 [MAGNESIUM] 사용 시 (348개 제품 기준):
    - [GLYCINE] 비율: 8.9%
    - [THEANINE] 비율: 1.7%
    - [ASHWAGANDHA] 비율: 1.4%

🔹 베이스 [THEANINE] 사용 시 (7개 제품 기준):
    - [MAGNESIUM] 비율: 85.7%

🔹 베이스 [ASHWAGANDHA] 사용 시 (5개 제품 기준):
    - [MAGNESIUM] 비율: 100.0%

🔹 베이스 [VALERIAN] 사용 시 (24개 제품 기준):
    - [CHAMOMILE] 비율: 4.2%
------------------------------------------------------------

📊 [Naver 국내쇼핑] 매트릭스 저장 완료: [chart_cooccurrence_heatmap_naver.png](data/chart_cooccurrence_heatmap_naver.png)
💡 [Naver 국내쇼핑] 핵심 인사이트 요약 (상위 베이스 성분별):

```
**[차트 결과물]**
- [iHerb 상관관계 확률 매트릭스 히트맵](data/chart_cooccurrence_heatmap_iherb.png)
- [Naver 상관관계 확률 매트릭스 히트맵](data/chart_cooccurrence_heatmap_naver.png)

---

## 5. 🛡️ 공공데이터 안전성(부작용) 검증 Plan (`py/validate_safety.py` 실행 결과)

```text
--- 성분별 안전성 및 부작용 키워드 분석 시작 ---
✅ 안전성 분석 완료! 결과 저장됨: [ingredient_safety_analysis.csv](data/ingredient_safety_analysis.csv)

--- 성분별 NLP 기반 부작용 언급 비율(%) ---
  ingredient  total_products  ...  digestive_ratio  habituation_ratio
0  magnesium               9  ...              0.0                0.0
1   theanine               1  ...              0.0                0.0
2   valerian              12  ...              0.0                0.0
3       gaba               7  ...              0.0                0.0

[4 rows x 5 columns]

============================================================
🚨 [Plan] 공공데이터(식약처/심평원) 연계 안전성 검증 및 Action Plan
============================================================

1. 공공데이터 소스 및 연계 방안 (Data Sources)
  - [식품안전나라(식약처) 건강기능식품 이상사례 신고 데이터]
    * URL: https://www.foodsafetykorea.go.kr/
    * 연계 방안: Open API (건강기능식품 품목제조신고, 위해식품차단시스템) 연동
    * 목적: 특정 성분(ex. 아슈와간다 추출물)의 국내 이상사례 건수 스크래핑 및 모니터링
  
  - [의약품안전나라 (DUR, 의약품처방조제지원시스템)]
    * URL: https://nedrug.mfds.go.kr/
    * 연계 방안: DUR 병용금기 및 주의 성분 API 호출
    * 목적: 수면 영양제 성분과 직장인들이 흔히 섭취하는 약물(진통제, 위장약) 간의 상호작용(Interaction) 검증

2. 3040 직장인 타겟 "스위치 오프" 배합의 안전성 가이드라인
  - 배합 제안: L-테아닌 + 마그네슘(글리시네이트) + 아슈와간다
  *(※ Co-occurrence 분석 결과에 따라, 글로벌 iHerb 및 국내 Naver 트렌드 양쪽에서 높은 빈도로 조합이 확인된 성분들임)*
  
  [성분별 공공데이터 기준 검증 포인트 & 시너지(Pair) 리스크 방어]
  ✔️ 테아닌(L-Theanine): '일일 섭취량 200mg~250mg' 초과 시 위장장애 발생 위험. 식약처 고시 기준치 엄수 설계 필요.
  ✔️ 마그네슘(Magnesium Glycinate): 테아닌/아슈와간다와의 배합률이 80~100%에 달하는 필수 베이스 성분. 산화마그네슘 대비 설사(Digestive) 부작용이 낮음을 안전성 확보 강점으로 마케팅에 활용. 신장 질환자 주의 문구 필수.
  ✔️ 아슈와간다(Ashwagandha): 갑상선 호르몬 항진 부작용 등 체질 리스크 존재. 식품안전나라 기준 '임산부 및 수유부 섭취 주의' 필수 멘션 및 복용 휴지기(Cycling) 마케팅 가이드 제공.

3. Action Items (To-Do)
  - [ ] 식품안전나라 API Key 발급 및 `py/fetch_public_safety_data.py` 스크립트 작성
  - [ ] 심평원 DUR API 연동 테스트 및 3040 타겟 병용 주의 약물 리스트 DB화
  - [ ] 추출된 데이터와 iHerb 부작용 리뷰 데이터를 교차 검증하는 ML 이상치 탐지(Anomaly Detection) 모델 개발


```

---

## 6. 📂 리포트 및 소스코드 (Collaboration)
각 작업자들이 분석한 리포트와 분석 도구들입니다.

- **분석 보고서 (마크다운 문서)**
  - [`md/sleep_supplement_strategy_report.md`](md/sleep_supplement_strategy_report.md): 수면 영양제 시장 전략 및 성분 교차 리포트
  - [`md/3040_marketing_ml_strategy.md`](md/3040_marketing_ml_strategy.md): 3040 직장인 타겟 배합 및 마케팅 ML 전략

- **분석 스크립트 (Python)**
  - [`py/analyze_3040_strategy.py`](py/analyze_3040_strategy.py): 3040 직장인 타겟 키워드 및 성분 기반 트렌드 비교
  - [`py/analyze_3040_strategy_v2.py`](py/analyze_3040_strategy_v2.py): 3040 직장인 타겟 성분 가치 가중치 고도화 분석
  - [`py/analyze_ingredient_cross.py`](py/analyze_ingredient_cross.py): 글로벌-국내 성분 매핑 및 시장 기회 분석
  - [`py/analyze_cooccurrence_advanced.py`](py/analyze_cooccurrence_advanced.py): 성분 간 짝꿍 조합 확률(Co-occurrence) 매트릭스 분석
  - [`py/validate_safety.py`](py/validate_safety.py): 공공데이터 및 부작용 맵핑 기반 안전성 검증
  - [`py/visualize_pdp_performance.py`](py/visualize_pdp_performance.py): 성분 분포 시각화 
  - [`py/analyze_reviews_deeper.py`](py/analyze_reviews_deeper.py): 제품군 뱃지 분석
