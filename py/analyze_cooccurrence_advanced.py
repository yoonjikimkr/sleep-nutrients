import os
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from collections import Counter

# macOS 기본 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

# 데이터 소스 경로
DB_PATH = os.path.join(DATA_DIR, "iherb_sleep.db")
IHERB_DETAILED_CSV = os.path.join(DATA_DIR, "iherb_sleep_products_detailed.csv")
NAVER_SLEEP_SUPPLEMENTS = os.path.join(DATA_DIR, "sleep_supplements.csv")

# 3040 타겟 최적화 및 겹치는 성분 (분석 대상 핵심 원료 풀)
TARGET_INGREDIENTS = [
    'magnesium', 'theanine', 'valerian', 'gaba', 
    'ashwagandha', 'lemon balm', 'chamomile', 'glycine', 
    'melatonin', '5-htp', 'tryptophan', 'vitamin b6'
]

def map_ingredient_name(raw_name):
    """원시 성분명(텍스트)에서 핵심 타겟 성분 키워드 추출 (단순화된 정규화)"""
    if not isinstance(raw_name, str): return None
    raw_name = raw_name.lower().strip()
    
    for target in TARGET_TARGET_INGREDIENTS: # Typo -> TARGET_INGREDIENTS
        pass # Will fix in next iteration if needed, fixing here directly
    
    for target in TARGET_INGREDIENTS:
        if target in raw_name:
            if target == 'magnesium glycinate': return 'magnesium' # 대표성분 분류
            if target == '5-htp': return '5-htp'
            if target == 'vitamin b6': return 'vitamin b6'
            return target
    return None

def extract_ingredients(text_series):
    """텍스트 군에서 성분 리스트 추출"""
    mapped_list = []
    for text in text_series.dropna():
        # 간단하게 텍스트 내에서 주요 키워드가 발견되면 해당 제품의 성분으로 간주
        product_ings = set()
        for target in TARGET_INGREDIENTS:
            if target in str(text).lower():
                product_ings.add(target)
        if product_ings:
            mapped_list.append(list(product_ings))
    return mapped_list

def compute_cooccurrence(ingredients_lists, title_prefix, file_suffix):
    if not ingredients_lists:
        print(f"\n⚠️ [{title_prefix}] 분석 대상 제품이 없습니다.")
        return

    n = len(TARGET_INGREDIENTS)
    co_matrix = pd.DataFrame(np.zeros((n, n)), index=TARGET_INGREDIENTS, columns=TARGET_INGREDIENTS)
    ing_counts = Counter()

    for ings in ingredients_lists:
        for ing in ings:
            ing_counts[ing] += 1
        
        if len(ings) >= 2:
            for ing1, ing2 in combinations(sorted(set(ings)), 2):
                co_matrix.loc[ing1, ing2] += 1
                co_matrix.loc[ing2, ing1] += 1 

    prob_matrix = pd.DataFrame(np.zeros((n, n)), index=TARGET_INGREDIENTS, columns=TARGET_INGREDIENTS)
    
    for row_ing in TARGET_INGREDIENTS:
        total_row_count = ing_counts.get(row_ing, 0)
        for col_ing in TARGET_INGREDIENTS:
            if row_ing == col_ing:
                prob_matrix.loc[row_ing, col_ing] = 1.0 
            elif total_row_count > 0:
                prob_matrix.loc[row_ing, col_ing] = co_matrix.loc[row_ing, col_ing] / total_row_count
                
    plt.figure(figsize=(11, 9))
    sns.heatmap(prob_matrix * 100, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': '동시 출현 확률 (%)'})
    
    plt.title(f'[{title_prefix}] 3040 타겟 영양제 주요 성분 간 짝꿍 상관관계\n(가로축 베이스 성분이 세로축 성분과 얼마나 함께 쓰이는가)', fontsize=14, pad=15)
    plt.xlabel('짝꿍 성분 (Co-ingredient)', fontsize=12)
    plt.ylabel('기준 성분 (Base Ingredient)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    output_path = os.path.join(DATA_DIR, f'chart_cooccurrence_heatmap_{file_suffix}.png')
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"\n📊 [{title_prefix}] 매트릭스 저장 완료: {output_path}")
    print(f"💡 [{title_prefix}] 핵심 인사이트 요약 (상위 베이스 성분별):")
    
    bases = ['magnesium', 'theanine', 'ashwagandha', 'valerian']
    for base in bases:
        if base in prob_matrix.index and ing_counts.get(base, 0) > 0:
            top_partners = prob_matrix.loc[base].drop(base).sort_values(ascending=False).head(3)
            print(f"\n🔹 베이스 [{base.upper()}] 사용 시 ({ing_counts[base]}개 제품 기준):")
            for partner, prob in top_partners.items():
                if prob > 0:
                    print(f"    - [{partner.upper()}] 비율: {prob*100:.1f}%")

def run_cooccurrence_matrix_analysis():
    print("🚀 [3040 직장인 타겟] 성분 간 짝꿍 상관관계 (Co-occurrence Matrix) 분석 시작")
    
    iherb_lists = []
    naver_lists = []

    # 소스 1: iHerb DB
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            # active_ingredients 컬럼이 없었으므로 ingredient_snippet에서만 가져오도록 쿼리 수정
            df_db = pd.read_sql_query("SELECT product_name, ingredient_snippet FROM iherb_sleep_products", conn)
            conn.close()
            db_texts = df_db['product_name'].fillna('') + " " + df_db['ingredient_snippet'].fillna('')
            iherb_lists.extend(extract_ingredients(db_texts))
            print(f" -> iHerb DB 로드 완료: {len(df_db)}개 제품")
        except Exception as e:
            print(f" -> iHerb DB 로드 실패: {e}")
            
    # 소스 2: iHerb Detailed CSV
    if os.path.exists(IHERB_DETAILED_CSV):
        df_csv = pd.read_csv(IHERB_DETAILED_CSV)
        csv_texts = df_csv['product_name'].fillna('') + " " + (df_csv['active_ingredients'] if 'active_ingredients' in df_csv.columns else '') + " " + df_csv['ingredient_snippet'].fillna('')
        iherb_lists.extend(extract_ingredients(csv_texts))
        print(f" -> iHerb Detailed CSV 로드 완료: {len(df_csv)}개 제품")

    # 소스 3: Naver Sleep Supplements CSV
    if os.path.exists(NAVER_SLEEP_SUPPLEMENTS):
        df_naver = pd.read_csv(NAVER_SLEEP_SUPPLEMENTS)
        naver_texts = df_naver['title'].fillna('') + " " + (df_naver['tags'] if 'tags' in df_naver.columns else '')
        naver_lists.extend(extract_ingredients(naver_texts))
        print(f" -> Naver CSV 로드 완료: {len(df_naver)}개 제품")
        
    print(f"\n✅ iHerb 분석 유효제품: {len(iherb_lists)}건 / Naver 분석 유효제품: {len(naver_lists)}건 (중복포함)\n")

    compute_cooccurrence(iherb_lists, "iHerb 글로벌", "iherb")
    print("-" * 60)
    compute_cooccurrence(naver_lists, "Naver 국내쇼핑", "naver")

if __name__ == "__main__":
    run_cooccurrence_matrix_analysis()
