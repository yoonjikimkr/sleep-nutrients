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
    
    # 성분 분류 (간이)
    ingredients = ['magnesium', 'melatonin', 'theanine', 'valerian', 'tryptophan', 'glycine', 'gaba']
    
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
    print("\n--- 성분별 부작용 언급 비율(%) ---")
    print(safety_df[['ingredient', 'total_products', 'drowsiness_ratio', 'digestive_ratio', 'habituation_ratio']])

if __name__ == "__main__":
    validate_safety()
