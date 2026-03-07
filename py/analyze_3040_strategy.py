import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (macOS)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
IHERB_CSV = os.path.join(DATA_DIR, "iherb_sleep_products_detailed.csv")
NAVER_SHOP_PATTERN = os.path.join(DATA_DIR, "shop_*.csv")

# 1. 3040 직장인 관련 키워드 정의
TARGET_KEYWORDS = ['stress', 'relaxation', 'calm', 'relax', 'anxiety', 'cortisol', 'adrenal', 'mood', 'focus']
KOR_KEYWORDS = ['직장인', '스트레스', '회사', '업무', '회사원', '공부', '야근', '피로']

def analyze_3040_strategy():
    print("🚀 3040 직장인 타겟 심층 분석 시작 (iHerb vs Naver)")
    
    # --- Part 1. iHerb 글로벌 트렌드 (고민 해결 기반) ---
    df_iherb = pd.read_csv(IHERB_CSV)
    
    # 3040 직장인 고민(Stress/Relax) 제품 필터링
    # 텍스트 데이터 준비 (상품명 + 설명 조각)
    df_iherb['text_corpus'] = (df_iherb['product_name'].fillna('') + ' ' + df_iherb['ingredient_snippet'].fillna('')).str.lower()
    
    mask = df_iherb['text_corpus'].apply(lambda x: any(kw in x for kw in TARGET_KEYWORDS))
    df_target = df_iherb[mask].copy()
    
    print(f"✅ iHerb에서 3040 관련 키워드를 포함한 상품 {len(df_target)}개를 발견했습니다.")
    
    # 해당 타겟 제품들이 공통적으로 사용하는 성분(Pair) 분석
    # active_ingredients 리스트화
    df_target['ing_list'] = df_target['active_ingredients'].dropna().apply(lambda x: [i.strip() for i in x.strip('[]').replace('"', '').split(', ')])
    
    # 성분들의 빈도 및 듀오(Pair) 분석
    from collections import Counter
    from itertools import combinations
    
    all_pairs = []
    all_ings = []
    
    for ings in df_target['ing_list']:
        if not isinstance(ings, list): continue
        ings = [i for i in ings if i and isinstance(i, str)]
        ings = sorted(list(set(ings))) # 중복 제거 및 정렬
        all_ings.extend(ings)
        if len(ings) >= 2:
            all_pairs.extend(list(combinations(ings, 2)))
            
    pair_counts = Counter(all_pairs).most_common(10)
    ing_counts = Counter(all_ings).most_common(10)
    
    print("\n💡 [iHerb] 3040 직장인 타겟의 글로벌 베스트 성분 조합 (Pairs):")
    for pair, count in pair_counts:
        print(f" - {pair[0]} + {pair[1]}: {count}개 제품")

    # --- Part 2. Naver 국내 트렌드 (실제 구매 키워드) ---
    import glob
    naver_files = glob.glob(NAVER_SHOP_PATTERN)
    df_naver_list = []
    for f in naver_files:
        df_temp = pd.read_csv(f)
        df_naver_list.append(df_temp)
    df_naver = pd.concat(df_naver_list, ignore_index=True)
    
    # 제목에서 직장인 관련 키워드 포함 상품 추출
    naver_mask = df_naver['title'].apply(lambda x: any(kw in x for kw in KOR_KEYWORDS))
    df_naver_target = df_naver[naver_mask]
    
    print(f"\n✅ 네이버 쇼핑에서 3040 관련 상품 {len(df_naver_target)}개를 분석 중입니다.")
    
    # 국내 타겟 상품의 평균 가격 및 리뷰 수 비교
    avg_price = df_naver_target['lprice'].astype(float).mean() if 'lprice' in df_naver_target else 0
    print(f"💰 국내 3040 타겟 상품 평균가: {avg_price:,.0f}원")

    # --- Part 3. 시각화 (성분 조합 매트릭스) ---
    # 간단한 Bar 차트로 상위 조합 시각화
    plt.figure(figsize=(12, 6))
    pair_labels = [f"{p[0]}+{p[1]}" for p, c in pair_counts]
    pair_values = [c for p, c in pair_counts]
    
    sns.barplot(x=pair_values, y=pair_labels, palette='magma')
    plt.title('3040 직장인 고민 해결을 위한 글로벌 성분 조합 TOP 10', fontsize=16)
    plt.xlabel('사용된 제품 수(SKU)', fontsize=12)
    plt.tight_layout()
    chart_path = os.path.join(DATA_DIR, 'chart_3040_ingredient_pairs.png')
    plt.savefig(chart_path, dpi=300)
    plt.close()
    
    print(f"\n📊 분석 차트 저장 완료: {chart_path}")
    
    # --- 결과 제안 (3040 Winning Formula) ---
    top_formula = pair_counts[0][0] if pair_counts else ("Magnesium", "Theanine")
    print(f"\n🎯 [결론] 3040 직장인 타겟의 Winning Formula 제안:")
    print(f" - 핵심 베이스: {top_formula[0]} & {top_formula[1]}")
    print(f" - 마케팅 전략: '퇴근 후 스위치 OFF' + '코르티솔(스트레스 호르몬) 케어' 강조")

if __name__ == "__main__":
    analyze_3040_strategy()
