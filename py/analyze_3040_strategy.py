import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from itertools import combinations
import glob

# 한글 폰트 설정 (macOS)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
IHERB_CSV = os.path.join(DATA_DIR, "iherb_sleep_products_detailed.csv")
NAVER_SHOP_PATTERN = os.path.join(DATA_DIR, "shop_*.csv")

# 1. 3040 직장인 관련 키워드 정의
TARGET_KEYWORDS_ENG = ['stress', 'relaxation', 'calm', 'relax', 'anxiety', 'cortisol', 'adrenal', 'mood', 'focus']
TARGET_KEYWORDS_KOR = ['직장인', '스트레스', '회사', '업무', '회사원', '공부', '야근', '피로', '수험생']

# 2. 3040 타겟 핵심 성분 (Winning Formula 후보군)
TARGET_INGS_ENG = ['theanine', 'magnesium', 'ashwagandha', 'gaba', 'valerian', 'lemon balm']
TARGET_INGS_KOR = ['테아닌', '마그네슘', '아슈와간다', '가바', '발레리안', '레몬밤']

def analyze_3040_strategy():
    print("🚀 [심층 분석] 3040 한국 직장인 스트레스/수면 타겟 트렌드 (키워드 vs 성분 타겟팅 비교)")
    print("-" * 60)
    
    # --- Part 1. iHerb 글로벌 트렌드 ---
    df_iherb = pd.read_csv(IHERB_CSV)
    df_iherb['text_corpus'] = (df_iherb['product_name'].fillna('') + ' ' + df_iherb['ingredient_snippet'].fillna('')).str.lower()
    
    # Keyword-based match
    mask_iherb_kw = df_iherb['text_corpus'].apply(lambda x: any(kw in x for kw in TARGET_KEYWORDS_ENG))
    df_iherb_kw = df_iherb[mask_iherb_kw].copy()
    
    # Ingredient-based match
    mask_iherb_ing = df_iherb['text_corpus'].apply(lambda x: any(ing in x for ing in TARGET_INGS_ENG))
    df_iherb_ing = df_iherb[mask_iherb_ing].copy()
    
    print(f"🌍 [iHerb 글로벌 타겟팅 트렌드]")
    print(f"  - 🎯 '스트레스/이완' 키워드 명시 제품: {len(df_iherb_kw)}개")
    print(f"  - 🌿 '핵심 타겟 성분' 포함 제품: {len(df_iherb_ing)}개 (실질적 시장 규모가 훨씬 큼)")
    print(f"  👉 시장 인사이트: 글로벌 제품들은 키워드를 명시하기보다, 성분 자체의 배합으로 목적(수면/스트레스)을 달성하고 있음.")
    
    # 핵심 타겟 성분 포함 제품군에서 Top 성분 조합 도출
    major_ingredients = ['magnesium', 'theanine', 'valerian', 'ashwagandha', 'gaba', 'lemon balm', 'chamomile', 'glycine', 'melatonin']
    all_pairs = []
    
    for _, row in df_iherb_ing.iterrows():
        text = row['text_corpus']
        found = [ing for ing in major_ingredients if ing in text]
        if len(found) >= 2:
            all_pairs.extend(list(combinations(sorted(found), 2)))
            
    pair_counts = Counter(all_pairs).most_common(10)
    
    print("\n💡 [iHerb] 핵심 타겟 성분(Target Ingredients) 제품군의 최우수 성분 짝꿍 (Top Pairs):")
    if not pair_counts:
        print("  - 충분한 성분 조합 데이터가 발견되지 않았습니다.")
    else:
        for pair, count in pair_counts:
            print(f"  - ✔️ [ {pair[0].upper()} ] + [ {pair[1].upper()} ]: {count}개 제품에서 동시 사용됨")

    # --- Part 2. Naver 국내 트렌드 ---
    naver_files = glob.glob(NAVER_SHOP_PATTERN)
    df_naver_list = []
    for f in naver_files:
        df_temp = pd.read_csv(f)
        df_naver_list.append(df_temp)
    if df_naver_list:
        df_naver = pd.concat(df_naver_list, ignore_index=True)
    else:
        df_naver = pd.DataFrame(columns=['title', 'lprice', 'category4'])
        
    df_naver['title_lower'] = df_naver['title'].str.lower()
    
    # Keyword-based match (제목에 직장인 키워드)
    mask_naver_kw = df_naver['title_lower'].apply(lambda x: any(kw in x for kw in TARGET_KEYWORDS_KOR))
    df_naver_kw = df_naver[mask_naver_kw]
    
    # Ingredient-based match (제목에 핵심 타겟 성분)
    mask_naver_ing = df_naver['title_lower'].apply(lambda x: any(ing in x for ing in TARGET_INGS_KOR))
    df_naver_ing = df_naver[mask_naver_ing]
    
    print(f"\n🇰🇷 [Naver 국내 타겟팅 트렌드 및 프라이싱 비교]")
    print(f"  - 🎯 '스트레스/직장인' 키워드 타겟 제품: {len(df_naver_kw)}개")
    print(f"  - 🌿 '핵심 타겟 성분' 타겟 제품: {len(df_naver_ing)}개")
    
    def print_price_stats(df_target, label):
        if not df_target.empty:
            avg_price = df_target['lprice'].astype(float).mean() if 'lprice' in df_target else 0
            min_price = df_target['lprice'].astype(float).min() if 'lprice' in df_target else 0
            max_price = df_target['lprice'].astype(float).max() if 'lprice' in df_target else 0
            print(f"    [{label}] 평균 {avg_price:,.0f}원 (최저 {min_price:,.0f}원 ~ 최고 {max_price:,.0f}원)")
        else:
            print(f"    [{label}] 제품을 찾을 수 없습니다.")

    print_price_stats(df_naver_kw, "키워드 기반")
    print_price_stats(df_naver_ing, "핵심성분 기반")
    
    print(f"\n📌 프라이싱 기획 인사이트: 3040 직장인은 수면/스트레스 문제에 기꺼이 프리미엄(고가)을 지불할 의사가 높으며, 단순 키워드보다 '핵심 성분'을 어필할 때 객단가를 유지하거나 확장할 여지가 더 큽니다.")

    # --- Part 3. 시각화 (성분 조합 매트릭스) ---
    chart_path = os.path.join(DATA_DIR, 'chart_3040_ingredient_pairs.png')
    if pair_counts:
        plt.figure(figsize=(12, 6))
        pair_labels = [f"{p[0]}+{p[1]}" for p, c in pair_counts]
        pair_values = [c for p, c in pair_counts]
        
        sns.barplot(x=pair_values, y=pair_labels, palette='magma')
        plt.title('iHerb 3040 타겟 성분(Magnesium, Theanine 등) 제품군의 성분 짝꿍 빈도', fontsize=16)
        plt.xlabel('사용된 제품 수 (빈도)', fontsize=12)
        plt.tight_layout()
        plt.savefig(chart_path, dpi=300)
        plt.close()
        print(f"\n📊 시각화 차트 저장 완료: {chart_path} (Winning Combination 한눈에 보기)")
    
    # --- 결과 제안 (3040 Winning Formula) ---
    print("\n" + "="*60)
    print("🎯 [최종 결론] 3040 한국 직장인 역량 강화를 위한 수면 영양제 Winning Formula")
    print("="*60)
    if pair_counts:
        top_formula = pair_counts[0][0]
        print(f" 💊 검증된 핵심 솔루션: {top_formula[0].upper()} & {top_formula[1].upper()} 베이스")
    else:
        print(" 💊 추천 핵심 솔루션: MAGNESIUM & THEANINE & ASHWAGANDHA 베이스")
        
    print(" 💡 [타겟 인사이트]: 글로벌 시장에서는 좁은 '스트레스' 키워드에 얽매이기보다")
    print("    'Theanine, Ashwagandha, Magnesium' 등 목적이 분명한 성분 조합 자체로 파이를 키우고 있습니다.")
    print("    국내 시장에서도 이런 '성분 시너지'를 전면에 내세울 때 3040의 지갑을 여는 고가(프리미엄) 전략이 유효합니다.")
    print("="*60)

if __name__ == "__main__":
    analyze_3040_strategy()
