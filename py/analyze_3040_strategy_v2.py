import pandas as pd
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
IHERB_CSV = os.path.join(DATA_DIR, "iherb_sleep_products_detailed.csv")

# 성분명 정규화 맵 (영문 -> 한글)
INGREDIENT_MAP = {
    'magnesium': '마그네슘',
    'theanine': '테아닌',
    'valerian': '발레리안',
    'chamomile': '카모마일',
    'glycine': '글리신',
    'gaba': '가바',
    'tryptophan': '트립토판',
    'tart cherry': '타트체리',
    'lemon balm': '레몬밤',
    'ashwagandha': '아슈와간다',
    '5-htp': '5-htp',
    'magnesium glycinate': '킬레이트 마그네슘',
    'vitamin b6': '비타민 B6'
}

# 3040 직장인 니즈에 따른 가중치
INGREDIENT_SCORES = {
    'l-theanine': {'relevance': 10, 'logic': '스트레스 완화 및 알파파 유도로 퇴근 후 머리 식히기에 최적'},
    'ashwagandha': {'relevance': 9, 'logic': '스트레스 호르몬(코르티솔) 조절 대포 성분'},
    'magnesium glycinate': {'relevance': 9, 'logic': '흡수율이 높고 근육 이완과 심신 안정에 탁월'},
    'gaba': {'relevance': 8, 'logic': '각성된 뇌를 차분하게 만드는 억제성 신경전달물질'},
    'valerian root': {'relevance': 7, 'logic': '천연 수면제로 불릴 만큼 강력한 입면 효과'},
    '5-htp': {'relevance': 6, 'logic': '세로토닌-멜라토닌 경로를 자극하여 전반적 무드 개선'},
    'lemon balm': {'relevance': 7, 'logic': '불안 해소와 집중력/이완 상호작용에 우수한 보조제'},
    'vitamin b6': {'relevance': 8, 'logic': '에너지 대사와 수면 호르몬 합성에 필수 조효소'}
}

def detailed_3040_needs_analysis():
    print("🎯 [3040 직장인 타겟 고도화 EDA]")
    
    df = pd.read_csv(IHERB_CSV)
    df['text_corpus'] = (df['product_name'].fillna('') + ' ' + df['ingredient_snippet'].fillna('')).str.lower()
    
    results = []
    for ing, data in INGREDIENT_SCORES.items():
        # iHerb에서의 출현 빈도 (시장에서의 검증도)
        market_count = df['text_corpus'].str.contains(ing.replace('-', ' ').replace(' root', ''), case=False, na=False).sum()
        
        # 3040 타겟 적합도 (가중치 x 시장빈도)
        strategy_score = data['relevance'] * (1 + (market_count / len(df)))
        
        # 한글명 매핑
        kor_name = INGREDIENT_MAP.get(ing.replace('l-', '').replace(' root', '').replace('-', ' '), ing)
        if ing == 'l-theanine': kor_name = '테아닌'
        
        results.append({
            '성분(ENG)': ing.upper(),
            '성분(KOR)': kor_name,
            '전략적_가치': strategy_score,
            '근거': data['logic']
        })
        
    res_df = pd.DataFrame(results).sort_values('전략적_가치', ascending=False)
    
    print("\n💡 3040 직장인 맞춤형 성분 전략:")
    print(res_df[['성분(ENG)', '성분(KOR)', '전략적_가치', '근거']].to_string(index=False))
    
    top_3 = [f"{row['성분(KOR)']}({row['성분(ENG)']})" for _, row in res_df.head(3).iterrows()]
    print(f"\n🚀 [최종 제안] 3040 직장인을 위한 '스위치 오프' 복합제 기획:")
    print(f" 📦 핵심 구성: {', '.join(top_3)}")
    print(f" 🏷️ 마케팅 키워드: #퇴근후5분 #코르티솔다이어트 #뇌전원끄기")

if __name__ == "__main__":
    detailed_3040_needs_analysis()
