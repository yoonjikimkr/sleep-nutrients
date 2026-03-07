import pandas as pd
import os
import sqlite3

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
DB_PATH = os.path.join(DATA_DIR, "iherb_sleep.db")

# 부작용/부정적 키워드 사전
SIDE_EFFECT_KEYWORDS = {
    'drowsiness': ['drowsy', 'sleepy next day', 'hangover', '졸음', '기상 후', '멍함', '잔여감'],
    'digestive': ['stomach', 'diarrhea', 'nausea', 'upset', '속쓰림', '설사', '소화', '위장'],
    'headache': ['headache', 'migraine', 'dizzy', '두통', '머리 아픔', '어지럼'],
    'habituation': ['addiction', 'withdrawal', 'dependent', '내성', '의존', '중독']
}

def validate_safety():
    print("--- 성분별 안전성 및 부작용 키워드 분석 시작 ---")
    
    # DB에서 제품 정보 로드
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT product_name, ingredient_snippet, badges FROM iherb_sleep_products", conn)
    conn.close()
    
    # 텍스트 통합
    df['text_corpus'] = (df['product_name'].fillna('') + ' ' + 
                         df['ingredient_snippet'].fillna('') + ' ' + 
                         df['badges'].fillna('')).str.lower()
    
    # 성분 분류 (3040 타겟 중심 확장)
    ingredients = [
        'magnesium', 'melatonin', 'theanine', 'valerian', 
        'tryptophan', 'glycine', 'gaba', 'ashwagandha', 'lemon balm', 'vitamin b6'
    ]
    
    results = []
    
    for ing in ingredients:
        ing_mask = df['text_corpus'].str.contains(ing, case=False, na=False)
        ing_df = df[ing_mask]
        
        if len(ing_df) == 0: continue
        
        ing_stats = {'ingredient': ing, 'total_products': len(ing_df)}
        
        for category, kws in SIDE_EFFECT_KEYWORDS.items():
            # 역설적으로 '부작용 없음'을 강조하는 문구일 수도 있으나, 
            # 여기서는 빈도 자체를 '리스크 노출도'로 파악
            match_count = ing_df['text_corpus'].apply(lambda t: any(kw in t for kw in kws)).sum()
            ing_stats[f'{category}_mentions'] = match_count
            ing_stats[f'{category}_ratio'] = (match_count / len(ing_df)) * 100
            
        results.append(ing_stats)
        
    safety_df = pd.DataFrame(results)
    output_path = os.path.join(DATA_DIR, "ingredient_safety_analysis.csv")
    safety_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"✅ 안전성 분석 완료! 결과 저장됨: {output_path}")
    print("\n--- 성분별 NLP 기반 부작용 언급 비율(%) ---")
    print(safety_df[['ingredient', 'total_products', 'drowsiness_ratio', 'digestive_ratio', 'habituation_ratio']])

def propose_public_data_safety_plan():
    """공공데이터(식약처, 심평원) 기반 부작용 검증 Action Plan 출력"""
    print("\n" + "="*60)
    print("🚨 [Plan] 공공데이터(식약처/심평원) 연계 안전성 검증 및 Action Plan")
    print("="*60)
    
    plan_text = """
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
  
  [성분별 공공데이터 기준 검증 포인트]
  ✔️ 테아닌(L-Theanine): '일일 섭취량 200mg~250mg' 초과 시 위장장애 발생 위험. 식약처 고시 기준치 엄수 설계 필요.
  ✔️ 마그네슘(Magnesium Glycinate): 산화마그네슘 대비 설사(Digestive) 부작용이 매우 낮음 (안전성 확보 강점 마케팅 활용). 신장 질환자 주의 문구 필수 기재.
  ✔️ 아슈와간다(Ashwagandha): 갑상선 호르몬 항진 부작용 등 체질에 따른 리스크 존재. 식품안전나라 기준 '임산부 및 수유부 섭취 주의' 필수 멘션 및 복용 휴지기(Cycling) 마케팅 가이드 제공.

3. Action Items (To-Do)
  - [ ] 식품안전나라 API Key 발급 및 `py/fetch_public_safety_data.py` 스크립트 작성
  - [ ] 심평원 DUR API 연동 테스트 및 3040 타겟 병용 주의 약물 리스트 DB화
  - [ ] 추출된 데이터와 iHerb 부작용 리뷰 데이터를 교차 검증하는 ML 이상치 탐지(Anomaly Detection) 모델 개발
"""
    print(plan_text)

if __name__ == "__main__":
    validate_safety()
    propose_public_data_safety_plan()
