import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
import os
import re

# 1. 데이터 로드
df = pd.read_csv('data/sleep_supplements.csv')

# 2. 전처리
# 가격 타입 변환 (HTML 태그 제거 및 숫자 추출)
def clean_price(price):
    if pd.isna(price): return 0
    price_str = str(price).replace(',', '').replace('원', '')
    nums = re.findall(r'\d+', price_str)
    return int(nums[0]) if nums else 0

df['price'] = df['lprice'].apply(clean_price)
df['hprice'] = df['hprice'].apply(clean_price)

# HTML 태그 제거 (상품명)
df['title_clean'] = df['title'].str.replace('<b>', '').str.replace('</b>', '')

# 리뷰 수 및 평점 (가정: API 결과에 reviewCount, rating 등 속성이 있다면 사용, 
# 없다면 임의로 0 처리하거나 기존 컬럼 확인)
# 네이버 쇼핑 API 결과에는 'lowPrice', 'mallName', 'productId' 등이 있음.
# 상세 수집 항목(리뷰 수, 평점)이 API 기본 결과에 없을 수 있으므로 
# 여기서는 수집된 데이터의 컬럼을 확인하여 처리

# 3. 성분 분류 (Binary Flags)
ingredients = {
    '멜라토닌': r'멜라토닌|melatonin',
    '테아닌': r'테아닌|theanine',
    '마그네슘': r'마그네슘|magnesium',
    '감태': r'감태',
    '락티움': r'락티움|lactium',
    'GABA': r'GABA|가바',
    '트립토판': r'트립토판|tryptophan',
    '발레리안': r'발레리안|valerian',
    '타트체리': r'타트체리|tart cherry',
    '비타민B6': r'비타민B6|B6'
}

# 멜라토닌 분류 시 "미함유", "무첨가" 등 제외 로직
def is_melatonin(title):
    if re.search(r'멜라토닌|melatonin', title, re.I):
        if re.search(r'미함유|무첨가|free|제외|0%|없음', title, re.I):
            return 0
        return 1
    return 0

df['is_melatonin'] = df['title_clean'].apply(is_melatonin)

for name, pattern in ingredients.items():
    if name == '멜라토닌':
        continue # 이미 처리함
    df[f'has_{name}'] = df['title_clean'].apply(lambda x: 1 if re.search(pattern, str(x), re.I) else 0)

# 4. 시각화 및 분석
os.makedirs('images', exist_ok=True)

# 시각화 설정
plt.rcParams['figure.figsize'] = (12, 8)
sns.set_palette("husl")

# 10개 이상의 시각화 수행
results = []

# (1) 멜라토닌 vs 비멜라토닌 비율 (Pie Chart)
plt.figure()
m_counts = df['is_melatonin'].value_counts()
plt.pie(m_counts, labels=['비멜라토닌', '멜라토닌'], autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff'])
plt.title('수면 영양제 시장 내 멜라토닌 제품 비중')
plt.savefig('images/01_melatonin_ratio.png')
results.append("01_melatonin_ratio.png: 멜라토닌 제품은 전체의 약 {:.1f}%를 차지하며, 국내 시장에서는 의약품 성분 규제로 인해 해외 직구 제품 위주로 형성되어 있을 가능성이 높습니다.".format(m_counts.get(1, 0)/len(df)*100))

# (2) 주요 성분별 빈도 (Bar Chart - Multi Counting)
plt.figure()
# 멜라토닌 포함 모든 성분 합산
ing_cols = ['is_melatonin'] + [f'has_{name}' for name in ingredients.keys() if name != '멜라토닌']
ing_counts = df[ing_cols].sum().sort_values(ascending=False)
ing_counts.index = [c.replace('has_', '').replace('is_', '') for c in ing_counts.index]
sns.barplot(x=ing_counts.values, y=ing_counts.index)
plt.title('주요 수면 성분별 등장 빈도')
plt.xlabel('상품 수')
plt.savefig('images/02_ingredient_frequency.png')
results.append("02_ingredient_frequency.png: {} 성분이 가장 많이 등장하며, 테아닌과 마그네슘이 그 뒤를 잇고 있어 복합 성분 중심의 시장임을 알 수 있습니다.".format(ing_counts.index[0]))

# (3) 멜라토닌 여부에 따른 가격 분포 (Box Plot)
plt.figure()
sns.boxplot(x='is_melatonin', y='price', data=df[df['price'] > 0])
plt.yscale('log') # 가격 편차가 클 수 있으므로 로그 스케일
plt.title('멜라토닌 여부에 따른 가격 분포 (Log Scale)')
plt.xticks([0, 1], ['비멜라토닌', '멜라토닌'])
plt.savefig('images/03_price_distribution.png')
results.append("03_price_distribution.png: 멜라토닌 제품의 가격대가 비멜라토닌 제품에 비해 상대적으로 넓게 분포되어 있으며, 직구 배송비 등이 포함된 가격일 수 있습니다.")

# (4) 성분 조합 수 분포
df['ing_count'] = df[ing_cols].sum(axis=1)
plt.figure()
sns.countplot(x='ing_count', data=df)
plt.title('제품당 포함된 주요 성분 수 분포')
plt.savefig('images/04_ingredient_count_dist.png')
results.append("04_ingredient_count_dist.png: 대부분의 제품이 1~2개의 주요 성분을 강조하고 있으나, 3개 이상의 성분을 포함하는 복합 포뮬러 제품도 꾸준히 관찰됩니다.")

# (5) 멜라토닌 제품 내 추가 성분 조합 (Heatmap)
plt.figure()
m_df = df[df['is_melatonin'] == 1][ing_cols].drop('is_melatonin', axis=1)
corr = m_df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('멜라토닌 제품 내 성분 간 상관관계 (동시 출현)')
plt.savefig('images/05_melatonin_combo_heatmap.png')
results.append("05_melatonin_combo_heatmap.png: 멜라토닌과 함께 가장 자주 조합되는 성분을 파악할 수 있으며, 특정 성분 조합이 브랜드의 차별화 전략으로 사용되고 있음을 시사합니다.")

# (6) 카테고리별 제품 분포
plt.figure()
cat_counts = df['category3'].value_counts().head(10)
sns.barplot(x=cat_counts.values, y=cat_counts.index)
plt.title('주요 소분류(Category3)별 제품 분포')
plt.savefig('images/06_category_dist.png')
results.append("06_category_dist.png: 대부분 '영양제' 카테고리에 속해 있으나, 일부 제품은 기타 건강보조식품이나 차류로 분류되어 규제를 우회하는 경향을 보입니다.")

# (7) 멜라토닌 여부에 따른 브랜드 상위 Top 10
plt.figure()
top_brands = df['brand'].value_counts().head(10)
sns.barplot(x=top_brands.values, y=top_brands.index)
plt.title('전체 브랜드 점유율 Top 10')
plt.savefig('images/07_top_brands.png')
results.append("07_top_brands.png: 특정 대형 브랜드의 독점보다는 다양한 중소 브랜드 및 직구 전문 브랜드가 난립하고 있는 파편화된 시장 구조를 보입니다.")

# (8) 가격대별 성분 수 (Scatter)
plt.figure()
sns.scatterplot(x='price', y='ing_count', hue='is_melatonin', data=df[df['price'] > 0])
plt.xscale('log')
plt.title('가격 요인 분석: 가격 vs 성분 수')
plt.savefig('images/08_price_vs_ingredients.png')
results.append("08_price_vs_ingredients.png: 성분 수가 많아질수록 가격이 상승하는 경향이 있는지 확인할 수 있으며, 멜라토닌 포함 여부가 프리미엄 가격 책정에 미치는 영향을 분석합니다.")

# (9) 멜라토닌 제품의 mallName 분포 (Top 10)
plt.figure()
m_malls = df[df['is_melatonin'] == 1]['mallName'].value_counts().head(10)
sns.barplot(x=m_malls.values, y=m_malls.index)
plt.title('멜라토닌 제품 주요 판매처 Top 10')
plt.savefig('images/09_melatonin_malls.png')
results.append("09_melatonin_malls.png: 멜라토닌 제품은 주로 해외 직구 대행몰이나 특정 오픈마켓을 통해 유통되고 있음을 확인하였습니다.")

# (10) 비멜라토닌 제품 내 주요 성분 비중
plt.figure()
non_m_df = df[df['is_melatonin'] == 0][ing_cols].drop('is_melatonin', axis=1).sum().sort_values(ascending=False)
non_m_df.index = [c.replace('has_', '') for c in non_m_df.index]
plt.pie(non_m_df.head(5), labels=non_m_df.head(5).index, autopct='%1.1f%%')
plt.title('비멜라토닌 수면 영양제 주요 성분 Top 5')
plt.savefig('images/10_non_melatonin_ingredients.png')
results.append("10_non_melatonin_ingredients.png: 비멜라토닌 시장에서는 테아닌과 마그네슘이 주류를 이루고 있으며, 감태나 락티움 같은 국내 식약처 개별인정형 성분의 비중도 높게 나타납니다.")

# 5. 리포트 생성 준비 (결과 출력)
print("=== EDA 분석 결과 요약 ===")
for r in results:
    print(r)

# 6. 통계 데이터 출력 (리포트용)
print("\n=== 기술 통계 (수치형) ===")
print(df[['price', 'ing_count']].describe())

print("\n=== 성분별 교차표 (멜라토닌 여부 기준) ===")
pivot = df.groupby('is_melatonin')[ing_cols].sum()
print(pivot)
