import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import os
import re
import json

# 1. 데이터 로드
print("1. 데이터 로드 중...")
df_insight = pd.read_csv("data/sleep_insight_3040.csv")
df_products = pd.read_csv("data/sleep_products_3040.csv")

# 2. 전처리
print("2. 데이터 전처리 중...")

# 2.1 상품명에서 평점, 리뷰수 등 수치 추출 (가정: lprice는 이미 숫자일 수 있음)
df_products['lprice'] = pd.to_numeric(df_products['lprice'], errors='coerce')

# 2.2 성분 분리 및 중복 카운팅 준비 (Explode)
# 'matched_ingredients' 컬럼은 "테아닌|마그네슘" 형태
df_ing_exploded = df_products.copy()
df_ing_exploded['ingredient'] = df_ing_exploded['matched_ingredients'].str.split('|')
df_ing_exploded = df_ing_exploded.explode('ingredient')

# 3. 시각화 설정
os.makedirs("images", exist_ok=True)
plt.style.use('ggplot') # seaborn 스타일 대신 ggplot 또는 기본 스타일
colors = plt.cm.Paired(np.linspace(0, 1, 12))

# --- 시각화 1: 시장 내 성분 노출 빈도 (공급 측면) ---
plt.figure(figsize=(10, 6))
ing_counts = df_ing_exploded['ingredient'].value_counts()
ing_counts.plot(kind='bar', color='skyblue')
plt.title("수면 영양제 시장 내 성분별 노출 빈도 (상품수)")
plt.xlabel("성분")
plt.ylabel("상품 수")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/01_ingredient_frequency.png")
plt.close()

# --- 시각화 2: 3040 인기 성분 추이 (수요 측면) ---
plt.figure(figsize=(12, 6))
for ing in df_insight['ingredient'].unique():
    subset = df_insight[df_insight['ingredient'] == ing]
    plt.plot(subset['period'], subset['ratio'], label=ing, marker='o', markersize=4)
plt.title("3040대 수면 영양제 성분별 클릭 지수 추이 (2024-2025)")
plt.xlabel("기간")
plt.ylabel("클릭 지수 (상대값)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/02_popularity_trend.png")
plt.close()

# --- 시각화 3: 성분별 평균 가격대 ---
plt.figure(figsize=(10, 6))
df_ing_exploded[df_ing_exploded['ingredient'] != '기타'].groupby('ingredient')['lprice'].mean().sort_values(ascending=False).plot(kind='bar', color='salmon')
plt.title("성분별 평균 가격 (단위: 원)")
plt.ylabel("평균 가격")
plt.tight_layout()
plt.savefig("images/03_avg_price_by_ingredient.png")
plt.close()

# --- 시각화 4: 브랜드 점유율 (상위 15개) ---
plt.figure(figsize=(10, 6))
df_products['brand'].value_counts().head(15).plot(kind='pie', autopct='%1.1f%%', colors=colors)
plt.title("수면 영양제 주요 브랜드 점유율 (상품 수 기준)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("images/04_brand_share.png")
plt.close()

# --- 시각화 5: 클릭 지수 합계 (총 수요 랭킹) ---
plt.figure(figsize=(10, 6))
df_insight.groupby('ingredient')['ratio'].sum().sort_values(ascending=False).plot(kind='barh', color='gold')
plt.title("성분별 총 클릭 지수 합계 (3040 수요 랭킹)")
plt.xlabel("총 클릭 지수")
plt.tight_layout()
plt.savefig("images/05_total_demand_rank.png")
plt.close()

# --- 시각화 6: 가격대 분포 (Histogram) ---
plt.figure(figsize=(10, 6))
plt.hist(df_products['lprice'].dropna(), bins=50, color='lightgreen', edgecolor='black')
plt.title("수면 영양제 가격대 분포")
plt.xlabel("가격(원)")
plt.ylabel("빈도")
# 이상치 제외를 위해 x축 제한 (예: 50만원 이하)
plt.xlim(0, 200000)
plt.tight_layout()
plt.savefig("images/06_price_distribution.png")
plt.close()

# --- 시각화 7: 성분별 상품 수 vs 클릭 지수 (Scatter) ---
demand = df_insight.groupby('ingredient')['ratio'].mean()
supply = df_ing_exploded[df_ing_exploded['ingredient'] != '기타']['ingredient'].value_counts()
common_ings = demand.index.intersection(supply.index)

plt.figure(figsize=(10, 6))
plt.scatter(supply[common_ings], demand[common_ings], s=100, color='purple', alpha=0.6)

# 인덱싱 방식 수정: labels, x, y를 바로 순회
for txt, x, y in zip(common_ings, supply[common_ings], demand[common_ings]):
    plt.annotate(txt, (x, y), fontsize=12, xytext=(5, 5), textcoords='offset points')
plt.title("성분별 공급(상품수) vs 수요(평균 클릭지수)")
plt.xlabel("상품 수 (공급)")
plt.ylabel("평균 클릭 지수 (수요)")
plt.grid(True)
plt.tight_layout()
plt.savefig("images/07_supply_vs_demand.png")
plt.close()

# --- 시각화 8: 쇼핑몰별 상품 분포 ---
plt.figure(figsize=(10, 6))
df_products['mallName'].value_counts().head(10).plot(kind='bar', color='orange')
plt.title("주요 판매 몰(Mall) 분포")
plt.ylabel("상품 수")
plt.tight_layout()
plt.savefig("images/08_mall_distribution.png")
plt.close()

# --- 시각화 9: 월별 클릭 총합 추이 ---
plt.figure(figsize=(12, 6))
df_insight.groupby('period')['ratio'].sum().plot(kind='line', marker='x', color='red')
plt.title("수면 영양제 전체 카테고리 월별 수요 추이 (3040)")
plt.ylabel("총 클릭 지수")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/09_monthly_demand_sum.png")
plt.close()

# --- 시각화 10: 성분 조합 빈도 (복합 성분 영양제 분석) ---
plt.figure(figsize=(10, 6))
df_products[df_products['matched_ingredients'].str.contains('|', regex=False)]['matched_ingredients'].value_counts().head(10).plot(kind='barh', color='brown')
plt.title("인기 성분 조합 (복합 영양제)")
plt.xlabel("상품 수")
plt.tight_layout()
plt.savefig("images/10_ingredient_combinations.png")
plt.close()

print("시각화 완료! images 폴더를 확인하세요.")

# --- 리포트용 통계 데이터 추출 ---
with open("data_summary.json", "w", encoding="utf-8") as f:
    summary = {
        "head": df_products.head().to_dict(),
        "tail": df_products.tail().to_dict(),
        "info": str(df_products.info()),
        "describe_price": df_products['lprice'].describe().to_dict(),
        "ing_counts": ing_counts.to_dict(),
        "top_demand": df_insight.groupby('ingredient')['ratio'].sum().sort_values(ascending=False).to_dict(),
        "brand_counts": df_products['brand'].value_counts().head(10).to_dict()
    }
    # json serialization issue fix for non-serializable types if any
    json.dump(summary, f, ensure_ascii=False, indent=4, default=str)

print("통계 요약 저장 완료.")
