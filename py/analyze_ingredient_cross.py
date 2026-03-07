import pandas as pd
import os
import json
import sqlite3

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
IHERB_CSV = os.path.join(DATA_DIR, "iherb_sleep_products_detailed.csv")
NAVER_SHOP_PATTERN = os.path.join(DATA_DIR, "shop_*.csv")

# 1. 성분명 표준화 매핑 (Canonical Korean Names) - 로버스트한 매핑
INGREDIENT_MAP = {
    'l-theanine': '테아닌', 'theanine': '테아닌', '테아닌': '테아닌',
    'valerian root': '발레리안 뿌리', 'valerian': '발레리안 뿌리', '발레리안': '발레리안 뿌리',
    'gaba': 'GABA', 'gamma aminobutyric acid': 'GABA', '가바': 'GABA',
    'ashwagandha': '아슈와간다', '아쉬아간다': '아슈와간다', '아슈와간다': '아슈와간다',
    '5-htp': '5-HTP', '5-히드록시트립토판': '5-HTP',
    'l-tryptophan': 'L-트립토판', 'tryptophan': 'L-트립토판', '트립토판': 'L-트립토판',
    'lemon balm': '레몬밤', '레몬밤': '레몬밤',
    'passionflower': '패션플라워', '시계꽃': '패션플라워', 'passion_flower': '패션플라워',
    'glycine': '글리신', '글리신': '글리신',
    'chamomile': '캐모마일', '캐모마일': '캐모마일',
    'taurine': '타우린', '타우린': '타우린',
    'inositol': '이노시톨', '이노시톨': '이노시톨',
    'tart cherry': '타트체리', '타트체리': '타트체리', 'tart_cherry': '타트체리',
    'lactium': '락티움', '락티움': '락티움',
    'melatonin': '멜라토닌', '멜라토닌': '멜라토닌',
    'magnesium': '마그네슘', '마그네슘': '마그네슘',
    'ecklonia cava': '감태추출물', 'ecklonia_cava': '감태추출물',
    '감태': '감태추출물', '감태추출물': '감태추출물',
    '미강': '미강주정추출물', '미강주정추출물': '미강주정추출물',
    '흑하랑': '흑하랑 상추', '락투신': '흑하랑 상추',
    'phytomelatonin': '식물성 멜라토닌', '식물성 멜라토닌': '식물성 멜라토닌'
}

import re

def extract_ingredients(text):
    if pd.isna(text):
        return []
    found = []
    text_lower = str(text).lower()
    for eng, kor in INGREDIENT_MAP.items():
        if re.search(f'\\b{re.escape(eng)}\\b', text_lower) or eng in text_lower:
            found.append(kor)
    return list(set(found))

def analyze_cross_ingredients():
    print("--- iHerb & Naver 성분 교집합 분석 시작 ---")
    
    # 1. iHerb 데이터 로드
    df_iherb = pd.read_csv(IHERB_CSV)
    
    # 성분 리스트 추출
    df_iherb['combined_text'] = (df_iherb['product_name'].fillna('') + ' ' + df_iherb['active_ingredients'].fillna('')).str.lower()
    df_iherb['ingredients_kor'] = df_iherb['combined_text'].apply(extract_ingredients)
    
    iherb_ingredients = df_iherb.explode('ingredients_kor')['ingredients_kor'].value_counts().reset_index()
    iherb_ingredients.columns = ['ingredient_kor', 'iherb_count']
    
    # 2. 네이버 데이터 로드
    import glob
    naver_files = glob.glob(os.path.join(DATA_DIR, "shop_*.csv"))
    df_naver_list = []
    for f in naver_files:
        df_temp = pd.read_csv(f)
        df_naver_list.append(df_temp)
    
    df_naver = pd.concat(df_naver_list, ignore_index=True)
    
    # 상품명에서 성분 추출
    df_naver['ingredients_kor'] = df_naver['title'].apply(extract_ingredients)
    naver_ingredients = df_naver.explode('ingredients_kor')['ingredients_kor'].value_counts().reset_index()
    naver_ingredients.columns = ['ingredient_kor', 'naver_count']

    
    # 3. 통합 매핑 (Outer Join)
    merged = pd.merge(iherb_ingredients, naver_ingredients, on='ingredient_kor', how='outer').fillna(0)
    
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
