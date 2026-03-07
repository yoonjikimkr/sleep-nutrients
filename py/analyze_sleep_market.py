import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import koreanize_matplotlib
import re

# 플랫폼별 데이터 경로
data_dir = "/Users/haileynoh/Documents/fcicb7/sleep/data"
image_dir = "/Users/haileynoh/Documents/fcicb7/sleep/images"
os.makedirs(image_dir, exist_ok=True)

naver_file = os.path.join(data_dir, "sleep_supplements.csv")
iherb_detailed_file = os.path.join(data_dir, "iherb_sleep_products_detailed.csv")

# 1. 성분명 표준화 매핑 (Canonical Korean Names)
ingredient_map = {
    'l-theanine': '테아닌', 'theanine': '테아닌', '테아닌': '테아닌',
    'valerian root': '발레리안 뿌리', 'valerian': '발레리안 뿌리', '발레리안': '발레리안 뿌리',
    'gaba': 'GABA', 'gamma aminobutyric acid': 'GABA', '가바': 'GABA',
    'ashwagandha': '아쉬아간다', '아쉬아간다': '아쉬아간다', '아슈와간다': '아쉬아간다',
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
    '흑하랑': '흑하랑 상추', '락투신': '흑하랑 상추'
}

def extract_ingredients(text):
    if pd.isna(text):
        return []
    found = []
    text_lower = str(text).lower()
    for eng, kor in ingredient_map.items():
        # 단어 경계(영문) 또는 단순 포함(한글) 체크
        if re.search(f'\\b{re.escape(eng)}\\b', text_lower) or eng in text_lower:
            found.append(kor)
    return list(set(found))

# 1. Naver 데이터 처리
print("Processing Naver data...")
df_naver = pd.read_csv(naver_file)
df_naver['ingredients'] = df_naver['title'].apply(extract_ingredients)
naver_ingredients = df_naver.explode('ingredients')['ingredients'].value_counts().reset_index()
naver_ingredients.columns = ['ingredient', 'naver_count']

# 2. iHerb 데이터 처리 (Detailed CSV 사용)
print("Processing iHerb detailed data...")
df_iherb = pd.read_csv(iherb_detailed_file)
# active_ingredients, main_active, product_name 컬럼 모두 활용
df_iherb['combined_text'] = (
    df_iherb['product_name'].fillna('') + ' ' + 
    df_iherb['active_ingredients'].fillna('') + ' ' + 
    df_iherb['main_active'].fillna('')
)
df_iherb['ingredients'] = df_iherb['combined_text'].apply(extract_ingredients)
iherb_ingredients = df_iherb.explode('ingredients')['ingredients'].value_counts().reset_index()
iherb_ingredients.columns = ['ingredient', 'iherb_count']

# 3. 데이터 병합 및 점유율 계산
merged = pd.merge(naver_ingredients, iherb_ingredients, on='ingredient', how='outer').fillna(0)

# 점유율 계산 (플랫폼별 전체 발견된 유효 성분 횟수 대비 %)
# 참고: 한 제품에 여러 성분이 있을 수 있으므로 성분의 '출현 비중'임
merged['naver_share'] = (merged['naver_count'] / merged['naver_count'].sum()) * 100
merged['iherb_share'] = (merged['iherb_count'] / merged['iherb_count'].sum()) * 100

# 전체 성분 데이터 수집 (정렬)
merged['total_count'] = merged['naver_count'] + merged['iherb_count']
final_df = merged.sort_values('total_count', ascending=False)

# 4. 시각화 (상위 25개 시각화)
plot_df = final_df.head(25)

plt.figure(figsize=(10, 12))
y = np.arange(len(plot_df))
height = 0.35

plt.barh(y + height/2, plot_df['naver_share'], height, label='네이버 쇼핑', color='#03C75A') 
plt.barh(y - height/2, plot_df['iherb_share'], height, label='iHerb', color='#FF9900') 

plt.yticks(y, plot_df['ingredient'])
plt.xlabel('성분별 점유 비중 (%)')
plt.title('네이버 쇼핑 vs iHerb 수면 영양제 주요 성분 분포 (멜라토닌/마그네슘 포함)')
plt.legend(title='플랫폼')
plt.gca().invert_yaxis() 

plt.tight_layout()
plt.savefig(os.path.join(image_dir, "sleep_market_share_comparison.png"))
plt.close()

# 5. 결과 데이터 저장 (모든 성분 포함)
final_df.to_csv(os.path.join(data_dir, "sleep_ingredient_market_share.csv"), index=False)

# Diversity 계산
naver_diversity = len(merged[merged['naver_count'] > 0])
iherb_diversity = len(merged[merged['iherb_count'] > 0])

print(f"Naver Diversity (Unique Ingredients found): {naver_diversity}")
print(f"iHerb Diversity (Unique Ingredients found): {iherb_diversity}")
print("\nFinal Result (Top 20):")
print(final_df[['ingredient', 'naver_count', 'iherb_count', 'naver_share', 'iherb_share']].head(20).to_markdown(index=False))

