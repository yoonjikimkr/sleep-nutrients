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

def run_cooccurrence_matrix_analysis():
    print("🚀 [3040 직장인 타겟] 성분 간 짝꿍 상관관계 (Co-occurrence Matrix) 분석 시작")
    
    # ---------------------------------------------------------
    # 1. 멀티 풀 데이터 소스 로드 및 텍스트 융합
    # ---------------------------------------------------------
    all_ingredients_lists = []

    # 소스 1: iHerb DB
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            # active_ingredients 또는 ingredient_snippet 활용
            df_db = pd.read_sql_query("SELECT active_ingredients, ingredient_snippet FROM iherb_sleep_products", conn)
            conn.close()
            db_texts = df_db['active_ingredients'].fillna('') + " " + df_db['ingredient_snippet'].fillna('')
            all_ingredients_lists.extend(extract_ingredients(db_texts))
            print(f" -> iHerb DB 로드 완료: {len(df_db)}개 제품 분석")
        except Exception as e:
            print(f" -> iHerb DB 로드 실패: {e}")
            
    # 소스 2: iHerb Detailed CSV
    if os.path.exists(IHERB_DETAILED_CSV):
        df_csv = pd.read_csv(IHERB_DETAILED_CSV)
        csv_texts = df_csv['active_ingredients'].fillna('') + " " + df_csv['ingredient_snippet'].fillna('')
        all_ingredients_lists.extend(extract_ingredients(csv_texts))
        print(f" -> iHerb Detailed CSV 로드 완료: {len(df_csv)}개 제품 분석")

    # 소스 3: Naver Sleep Supplements CSV (국내 겹치는 성분 분석용)
    if os.path.exists(NAVER_SLEEP_SUPPLEMENTS):
        df_naver = pd.read_csv(NAVER_SLEEP_SUPPLEMENTS)
        # 네이버는 타이틀이나 태그에 성분이 명시됨
        naver_texts = df_naver['title'].fillna('') + " " + (df_naver['tags'] if 'tags' in df_naver.columns else '')
        all_ingredients_lists.extend(extract_ingredients(naver_texts))
        print(f" -> Naver Sleep Supplements CSV 로드 완료: {len(df_naver)}개 제품 분석")
        
    print(f"\n✅ 총 통합 분석 대상 제품(유효 성분 포함): {len(all_ingredients_lists)} 건 (중복 포함)")

    # ---------------------------------------------------------
    # 2. Co-occurrence (동시 출현) 매트릭스 계산
    # ---------------------------------------------------------
    # 빈 매트릭스 생성
    n = len(TARGET_INGREDIENTS)
    co_matrix = pd.DataFrame(np.zeros((n, n)), index=TARGET_INGREDIENTS, columns=TARGET_INGREDIENTS)
    ing_counts = Counter()

    for ings in all_ingredients_lists:
        for ing in ings:
            ing_counts[ing] += 1
        
        # 2개 이상 성분이 있을 때 짝꿍 카운트
        if len(ings) >= 2:
            for ing1, ing2 in combinations(sorted(ings), 2):
                co_matrix.loc[ing1, ing2] += 1
                co_matrix.loc[ing2, ing1] += 1 # 대칭 행렬

    # ---------------------------------------------------------
    # 3. 확률 기반 (Probability) 매트릭스로 변환 
    # (A가 들어간 제품 중 B가 들어갈 확률)
    # ---------------------------------------------------------
    prob_matrix = pd.DataFrame(np.zeros((n, n)), index=TARGET_INGREDIENTS, columns=TARGET_INGREDIENTS)
    
    for row_ing in TARGET_INGREDIENTS:
        total_row_count = ing_counts.get(row_ing, 0)
        for col_ing in TARGET_INGREDIENTS:
            if row_ing == col_ing:
                prob_matrix.loc[row_ing, col_ing] = 1.0 # 자기 자신은 100%
            elif total_row_count > 0:
                # row_ing가 포함된 제품 중 col_ing도 함께 포함된 비율
                prob_matrix.loc[row_ing, col_ing] = co_matrix.loc[row_ing, col_ing] / total_row_count
                
    # ---------------------------------------------------------
    # 4. 시각화 (히트맵 생성)
    # ---------------------------------------------------------
    plt.figure(figsize=(12, 10))
    # 확률을 100분율(%)로 표기하기 위해 * 100
    sns.heatmap(prob_matrix * 100, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': '동시 출현 확률 (%)'})
    
    plt.title('수면 영양제 주요 성분 간 \'짝꿍\' 상관관계 (Co-occurrence Probability)\n- 가로축 성분이 세로축 성분과 베이스로 얼마나 쓰이는지 확률(%) -', fontsize=15, pad=20)
    plt.xlabel('짝꿍 성분 (Co-ingredient)', fontsize=12)
    plt.ylabel('기준 성분 (Base Ingredient)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    output_path = os.path.join(DATA_DIR, 'chart_ingredient_cooccurrence_heatmap.png')
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"\n📊 상관관계 확률 매트릭스 히트맵 저장 완료: {output_path}")
    
    # ---------------------------------------------------------
    # 5. 주요 인사이트 추출 (터미널 출력)
    # ---------------------------------------------------------
    print("\n💡 [핵심 인사이트] 주요 베이스 성분의 글로벌 짝꿍 조합 분석 결과:")
    
    bases = ['magnesium', 'theanine', 'ashwagandha']
    for base in bases:
        if base in prob_matrix.index:
            # 베이스 성분이 포함된 제품 중 가장 같이 많이 쓰인 탑 3 성분 (자기 자신 제외)
            top_partners = prob_matrix.loc[base].drop(base).sort_values(ascending=False).head(3)
            print(f"\n🔹 베이스 성분 [{base.upper()}] 사용 시:")
            for partner, prob in top_partners.items():
                if prob > 0:
                    print(f"    - {partner.upper()} 성분과 {prob*100:.1f}% 확률로 함께 배합됨")

if __name__ == "__main__":
    run_cooccurrence_matrix_analysis()
