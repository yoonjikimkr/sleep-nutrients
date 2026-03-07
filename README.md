# 🌙 Sleep Nutrients Project

글로벌(iHerb) 및 국내(Naver) 데이터를 통합 분석하여, 최적의 수면 영양제 복합제 기획과 시장 전략을 수립하는 프로젝트입니다.

---

## 🎯 3040 직장인 타겟 심층 분석 결과 (`py/analyze_3040_strategy.py` 실행 결과)

```text
🚀 3040 직장인 타겟 심층 분석 시작 (iHerb vs Naver)
✅ iHerb에서 3040 관련 키워드를 포함한 상품 21개를 발견했습니다.

💡 [iHerb] 3040 직장인 타겟의 글로벌 베스트 성분 조합 (Pairs):

✅ 네이버 쇼핑에서 3040 관련 상품 39개를 분석 중입니다.
💰 국내 3040 타겟 상품 평균가: 63,389원

📊 분석 차트 저장 완료: /Users/kimyo/Documents/PARA/sleep-nutrients/data/chart_3040_ingredient_pairs.png

🎯 [결론] 3040 직장인 타겟의 Winning Formula 제안:
 - 핵심 베이스: Magnesium & Theanine
 - 마케팅 전략: '퇴근 후 스위치 OFF' + '코르티솔(스트레스 호르몬) 케어' 강조
```

## 🎯 3040 직장인 타겟 고도화 EDA 결과 (`py/analyze_3040_strategy_v2.py` 실행 결과)

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

## 🎯 3040 직장인 타겟 성분 짝꿍 매트릭스 (`py/analyze_cooccurrence_advanced.py` 실행 결과)

```text
🚀 [3040 직장인 타겟] 성분 간 짝꿍 상관관계 (Co-occurrence Matrix) 분석 시작
 -> iHerb DB 로드 실패: Execution failed on sql 'SELECT active_ingredients, ingredient_snippet FROM iherb_sleep_products': no such column: active_ingredients
 -> iHerb Detailed CSV 로드 완료: 432개 제품 분석
 -> Naver Sleep Supplements CSV 로드 완료: 842개 제품 분석

✅ 총 통합 분석 대상 제품(유효 성분 포함): 393 건 (중복 포함)

📊 상관관계 확률 매트릭스 히트맵 저장 완료: /Users/kimyo/Documents/PARA/sleep-nutrients/data/chart_ingredient_cooccurrence_heatmap.png

💡 [핵심 인사이트] 주요 베이스 성분의 글로벌 짝꿍 조합 분석 결과:

🔹 베이스 성분 [MAGNESIUM] 사용 시:
    - GLYCINE 성분과 9.1% 확률로 함께 배합됨
    - THEANINE 성분과 1.5% 확률로 함께 배합됨
    - ASHWAGANDHA 성분과 1.5% 확률로 함께 배합됨

🔹 베이스 성분 [THEANINE] 사용 시:
    - MAGNESIUM 성분과 83.3% 확률로 함께 배합됨

🔹 베이스 성분 [ASHWAGANDHA] 사용 시:
    - MAGNESIUM 성분과 100.0% 확률로 함께 배합됨
```

---

## 📂 리포트 및 소스코드 (Collaboration)
각 작업자들이 분석한 리포트와 분석 도구들입니다.

- **분석 보고서 (마크다운 문서)**
  - [`md/sleep_supplement_strategy_report.md`](md/sleep_supplement_strategy_report.md): 수면 영양제 시장 전략 및 성분 교차 리포트
  - [`md/iherb_sleep_presentation.md`](md/iherb_sleep_presentation.md): 프레젠테이션용 상세 정리
  - [`md/3040_marketing_ml_strategy.md`](md/3040_marketing_ml_strategy.md): 3040 직장인 타겟 배합 및 마케팅 ML 전략

- **분석 스크립트 (Python)**
  - `py/analyze_3040_strategy.py`: 3040 직장인 타겟 성분 조합 기본 분석
  - `py/analyze_3040_strategy_v2.py`: 3040 직장인 타겟 성분 가치 가중치 고도화 분석
  - `py/analyze_cooccurrence_advanced.py`: 성분 간 짝꿍 조합 확률(Co-occurrence) 매트릭스 분석
  - `py/analyze_ingredient_cross.py`: 글로벌-국내 성분 매핑 및 시장 기회 분석
  - `py/validate_safety.py`: 부작용 및 키워드 기반 안전성 검증 스캔
  - `py/visualize_pdp_performance.py`: 성분 분포 시각화 
  - `py/analyze_reviews_deeper.py`: 제품군 뱃지 분석
