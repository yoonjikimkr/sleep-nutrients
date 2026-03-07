import pandas as pd
import os
import json
import sqlite3

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
IHERB_CSV = os.path.join(DATA_DIR, "iherb_sleep_products_detailed.csv")
NAVER_SHOP_PATTERN = os.path.join(DATA_DIR, "shop_*.csv")

# 1. 성분명 정규화 맵 (영문 -> 한글 및 표준화)
INGREDIENT_MAP = {
    'magnesium': '마그네슘',
    'melatonin': '멜라토닌',
    'theanine': '테아닌',
    'valerian': '발레리안',
    'chamomile': '카모마일',
    'passionflower': '패션플라워',
    'glycine': '글리신',
    'gaba': '가바',
    'tryptophan': '트립토판',
    'tart cherry': '타트체리',
    'lemon balm': '레몬밤',
    'ashwagandha': '아슈와간다',
    '5-htp': '5-htp',
    'lactium': '락티움',
    'phytomelatonin': '식물성 멜라토닌'
}

def analyze_cross_ingredients():
    print("--- iHerb & Naver 성분 교집합 분석 시작 ---")
    
    # 1. iHerb 데이터 로드 (이미 가공된 active_ingredients 활용)
    df_iherb = pd.read_csv(IHERB_CSV)
    
    # 성분 리스트 추출 및 카운트
    # iherb_sleep_products_detailed.csv에는 'active_ingredients' 컬럼이 문자열 리스트 형태로 저장되어 있음
    all_iherb_ings = []
    for ings in df_iherb['active_ingredients'].dropna():
        # '["Magnesium", "Theanine"]' 형태를 리스트로 변환
        try:
            cleaned_ings = ings.strip('[]').replace('"', '').split(', ')
            all_iherb_ings.extend([ing.lower().strip() for ing in cleaned_ings])
        except:
            continue
            
    iherb_freq = pd.Series(all_iherb_ings).value_counts().reset_index()
    iherb_freq.columns = ['ingredient_eng', 'iherb_count']
    
    # 한글명 매핑
    iherb_freq['ingredient_kor'] = iherb_freq['ingredient_eng'].map(INGREDIENT_MAP)
    
    # 2. 네이버 데이터 로드 (shop_*.csv 파일들 통합)
    import glob
    naver_files = glob.glob(os.path.join(DATA_DIR, "shop_*.csv"))
    df_naver_list = []
    for f in naver_files:
        df_temp = pd.read_csv(f)
        df_naver_list.append(df_temp)
    
    df_naver = pd.concat(df_naver_list, ignore_index=True)
    
    # 상품명에서 성분 키워드 추출
    naver_ing_counts = {}
    for kor_name in INGREDIENT_MAP.values():
        count = df_naver['title'].str.contains(kor_name, case=False, na=False).sum()
        naver_ing_counts[kor_name] = count
        
    naver_freq = pd.DataFrame(list(naver_ing_counts.items()), columns=['ingredient_kor', 'naver_count'])
    
    # 3. 통합 매핑 (Outer Join)
    merged = pd.merge(iherb_freq, naver_freq, on='ingredient_kor', how='outer').fillna(0)
    
    # 4. 분석 인사이트 도출
    # - 글로벌 베스트 (iHerb count 높음) 이면서 국내 인지도 있음 (Naver count > 0)
    merged['opportunity_score'] = (merged['iherb_count'] * 0.4) + (merged['naver_count'] * 0.6)
    
    # 결과 저장
    merged_sorted = merged.sort_values('opportunity_score', ascending=False)
    output_path = os.path.join(DATA_DIR, "ingredient_cross_analysis.csv")
    merged_sorted.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"✅ 분석 완료! 결과 저장됨: {output_path}")
    print("\n--- 주요 성분 기회 요소 (Top 5) ---")
    print(merged_sorted[merged_sorted['ingredient_kor'] != '멜라토닌'].head(6)) # 멜라토닌 제외

if __name__ == "__main__":
    analyze_cross_ingredients()
