import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 플랫폼별 데이터 경로
data_dir = "/Users/haileynoh/Documents/fcicb7/sleep/data"
image_dir = "/Users/haileynoh/Documents/fcicb7/sleep/images"
os.makedirs(image_dir, exist_ok=True)

naver_file = os.path.join(data_dir, "sleep_supplements.csv")
iherb_freq_file = os.path.join(data_dir, "iherb_true_ingredient_frequency.csv")

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
    'tart cherry': '타트체리', '타트체리': '타트체리',
    'lactium': '락티움', '락티움': '락티움',
    'melatonin': '멜라토닌', '멜라토닌': '멜라토닌',
    'magnesium': '마그네슘', '마그네슘': '마그네슘',
    '감태': '감태추출물', '감태추출물': '감태추출물',
    '미강': '미강주정추출물', '미강주정추출물': '미강주정추출물',
    '흑하랑': '흑하랑 상추', '락투신': '흑하랑 상추'
}

# 분석 제외 성분
exclude_ingredients = ['멜라토닌', '마그네슘']

def extract_naver_ingredients(title):
    found = []
    title_lower = str(title).lower()
    for eng, kor in ingredient_map.items():
        if eng in title_lower:
            found.append(kor)
    return list(set(found))

# 1. Naver 데이터 처리
df_naver = pd.read_csv(naver_file)
df_naver['ingredients'] = df_naver['title'].apply(extract_naver_ingredients)
naver_ingredients = df_naver.explode('ingredients')['ingredients'].value_counts().reset_index()
naver_ingredients.columns = ['ingredient', 'naver_count']

# 2. iHerb 데이터 처리
df_iherb_freq = pd.read_csv(iherb_freq_file)
def map_iherb_name(name):
    name_lower = str(name).lower()
    for eng, kor in ingredient_map.items():
        if eng == name_lower: # iHerb 빈도 파일은 이미 토큰화되어 있으므로 sub-string보다는 exact match가 나음
            return kor
        if eng in name_lower:
            return kor
    return "기타"

df_iherb_freq['ingredient_kor'] = df_iherb_freq['ingredient_list'].apply(map_iherb_name)
iherb_ingredients = df_iherb_freq.groupby('ingredient_kor').agg({'n_products': 'sum'}).reset_index()
iherb_ingredients.columns = ['ingredient', 'iherb_count']
iherb_ingredients = iherb_ingredients[iherb_ingredients['ingredient'] != '기타']

# 3. 데이터 병합 및 필터링
merged = pd.merge(naver_ingredients, iherb_ingredients, on='ingredient', how='outer').fillna(0)
merged = merged[~merged['ingredient'].isin(exclude_ingredients)]

# 점유율 계산 (플랫폼별 전체 등장 횟수 대비 %)
merged['naver_share'] = (merged['naver_count'] / merged['naver_count'].sum()) * 100
merged['iherb_share'] = (merged['iherb_count'] / merged['iherb_count'].sum()) * 100

# 상위 성분 정렬 (전체 등장 빈도 기준)
merged['total_count'] = merged['naver_count'] + merged['iherb_count']
final_df = merged.sort_values('total_count', ascending=False)
if len(final_df) > 15:
    plot_df = final_df.head(15)
else:
    plot_df = final_df

# 4. 시각화
plt.figure(figsize=(10, 8))
y = np.arange(len(plot_df))
height = 0.35

plt.barh(y + height/2, plot_df['naver_share'], height, label='네이버 쇼핑', color='#03C75A') # Naver Green
plt.barh(y - height/2, plot_df['iherb_share'], height, label='iHerb', color='#FF9900') # iHerb Orange

plt.yticks(y, plot_df['ingredient'])
plt.xlabel('시장 점유 비중 (%)')
plt.title('수면 건강보조제 성분별 시장 점유 비중 비교 (멜라토닌/마그네슘 제외)')
plt.legend(title='플랫폼')
plt.gca().invert_yaxis() # 빈도순 내림차순 정렬

plt.tight_layout()
plt.savefig(os.path.join(image_dir, "sleep_market_share_comparison.png"))
plt.close()

# 5. 결과 데이터 저장
final_df.to_csv(os.path.join(data_dir, "sleep_ingredient_market_share.csv"), index=False)

# Diversity 계산
naver_diversity = len(merged[merged['naver_count'] > 0])
iherb_diversity = len(merged[merged['iherb_count'] > 0])

print(f"Naver Diversity: {naver_diversity}")
print(f"iHerb Diversity: {iherb_diversity}")
print(final_df[['ingredient', 'naver_share', 'iherb_share']].head(15).to_markdown(index=False))
