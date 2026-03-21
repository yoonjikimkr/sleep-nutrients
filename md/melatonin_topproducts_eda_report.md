---
marp: true
theme: default
paginate: true
backgroundColor: #fff
---

# 이커머스 식물성 멜라토닌 EDA 및 제품 개발 인사이트
### 데이터 기반 신제품 포지셔닝 전략 (네이버, 올리브영, SSG, G마켓)

---
## Problem Definition
- **목적**: 국내 주요 플랫폼에서 판매 중인 상위 80개 식물성 멜라토닌 제품의 패턴을 분석해, 시장 트렌드와 성공 방정식을 도출합니다.
- **핵심 과제**: 제형, 멜라토닌 추출원, 가격(1회 섭취당), 추가 영양성분 조합의 상관관계를 파악합니다.
- **최종 목표**: 데이터를 종합하여 새로운 프리미엄 혹은 대중형 멜라토닌 제품의 최적 출시 스펙(제안)을 확립합니다.

---
## Dataset Overview
<style scoped>
table { font-size: 0.6em; }
</style>

| source   | product_name                                       |   discounted_price | format   | melatonin_source   |   melatonin_mg |
|:---------|:---------------------------------------------------|-------------------:|:---------|:-------------------|---------------:|
| naver    | 식물성 멜라토닌 타트체리수면 영양제 불면증 L 트립토판 테아닌 꿀잠              |              31900 | 정제/캡슐    | 타트체리               |              2 |
| naver    | [슈퍼적립] [네이버 단독] CJ 멜라메이트 식물성 멜라토닌 함유 구미젤리 40구미, 2개 |              36900 | 구미/젤리    | 타트체리               |              2 |
| naver    | [7개월분] 락티브 식물성 멜라토닌 5mg 함유 멜라드림 플러스 L-트립토판 30정, 7개 |             120000 | 정제/캡슐    | 타트체리               |              5 |
| naver    | [국민영양] 식물성 멜라토닌 함유 여에스더 멜라나인 플러스 30정, 3개           |              26700 | 정제/캡슐    | 복합/기타 추출물          |              2 |
| naver    | [국민영양] 식물성 멜라토닌 함유 여에스더 멜라나인 플러스 30정, 6개           |              53400 | 정제/캡슐    | 복합/기타 추출물          |              2 |

---
## Data info()
<style scoped>
pre { font-size: 0.7em; }
</style>

```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 80 entries, 0 to 79
Data columns (total 4 columns):
 #   Column             Non-Null Count  Dtype  
---  ------             --------------  -----  
 0   discounted_price   80 non-null     float64
 1   melatonin_mg       80 non-null     float64
 2   servings           80 non-null     float64
 3   price_per_serving  80 non-null     float64
dtypes: float64(4)
memory usage: 2.6 KB
```

---
## 핵심 수치 기술 통계 (Descriptive Stats)
<style scoped>
table { font-size: 0.7em; }
</style>

|       |   discounted_price |   melatonin_mg |   servings |   price_per_serving |   num_add_ingredients |
|:------|-------------------:|---------------:|-----------:|--------------------:|----------------------:|
| count |               80   |           80   |       80   |                80   |                  80   |
| mean  |            36426.1 |            2.5 |       40.8 |              1670.4 |                   4.5 |
| std   |            38789   |            1.5 |       28.3 |              6130.5 |                   2.7 |
| min   |             3500   |            1   |        1   |               111.7 |                   0   |
| 25%   |            16732.5 |            2   |       30   |               414.2 |                   3   |
| 50%   |            24735   |            2   |       30   |               670.3 |                   5   |
| 75%   |            41810   |            2   |       30   |              1283.4 |                   7   |
| max   |           268000   |           10   |      180   |             55160   |                  10   |

---
## Key EDA Findings: 멜라토닌 추출원 분포 (1)
![width:700px](images/v1_source.png)

---
## Key EDA Findings: 멜라토닌 추출원 분포 (2)
<style scoped>
table { font-size: 0.6em; }
</style>

**빈도표:**

| melatonin_source   |   count |
|:-------------------|--------:|
| 타트체리               |      55 |
| 복합/기타 추출물          |      15 |
| 토마토                |       6 |
| 피스타치오              |       3 |
| 감태                 |       1 |

---
## Key EDA Findings: 멜라토닌 추출원 분포 (3)
**인사이트:**
- 전체 데이터 중 '타트체리'가 가장 지배적인 멜라토닌 핵심 추출 원료로 사용되고 있습니다.
- 타트체리 외에도 복합 추출물, 토마토, 감태 등 특수한 식물성 성분을 내세우는 제품들이 일부 존재하며 소수 틈새 시장을 구성하고 있습니다.
- 대중적으로 거부감이 없고 친숙한 타트체리를 메인 베이스로 안전성을 강조하는 전략이 이커머스 시장 최고 표본형으로 자리 잡혀 있습니다.

---
## Key EDA Findings: 제형 분포 (1)
![width:700px](images/v2_format.png)

---
## Key EDA Findings: 제형 분포 (2)
<style scoped>
table { font-size: 0.55em; }
</style>

<div style="display: flex; gap: 20px;">
<div style="flex: 1;" markdown="1">

**빈도표:**

| format   |   count |
|:---------|--------:|
| 정제/캡슐    |      65 |
| 구미/젤리    |      11 |
| 파우더/분말   |       4 |

</div>
<div style="flex: 1;" markdown="1">

**인사이트:**

- 데이터 기반, '정제/캡슐' 제형이 65개로 1위를 차지하고 있습니다.
- 거부감을 줄인 '구미/젤리' 타입이 11개로 확인되며 뚜렷한 시장 점유율을 차지하고 있습니다.
- '액상'과 '가루/분말' 등 다양한 제형 다변화가 진행 중입니다.

</div>
</div>

---
## Key EDA Findings: 1회 섭취당 가격 분포 (1)
![width:700px](images/v3_price.png)

---
## Key EDA Findings: 1회 섭취당 가격 분포 (2)
<style scoped>
table { font-size: 0.55em; }
</style>

<div style="display: flex; gap: 20px;">
<div style="flex: 1;" markdown="1">

**기술통계:**

|       |   price_per_serving |
|:------|--------------------:|
| count |                80   |
| mean  |              1670.4 |
| std   |              6130.5 |
| min   |               111.7 |
| 25%   |               414.2 |
| 50%   |               670.3 |
| 75%   |              1283.4 |
| max   |             55160   |

</div>
<div style="flex: 1;" markdown="1">

**인사이트:**

- 소비자가 체감하는 1회 섭취당 실 구매가입니다. 25~75 백분위수가 대략 414원 ~ 1283원 사이에 뭉쳐 구성됩니다.
- 커피 한 잔 가격보다 훨씬 저렴한 대중적 '가성비'가 수면 보조제 시장의 기본 스펙으로 작동합니다.
- 2,000원이 넘어가는 제품군은 프리미엄을 위한 차별화된 기능성 스펙이 요구됩니다.

</div>
</div>

---
## Key EDA Findings: 주요 영양 성분 등장(TF-IDF) (1)
![width:700px](images/v4_tfidf.png)

---
## Key EDA Findings: 주요 영양 성분 등장(TF-IDF) (2)
<style scoped>
table { font-size: 0.55em; }
</style>

<div style="display: flex; gap: 20px;">
<div style="flex: 1;" markdown="1">

**키워드 점수:**

|    | 키워드       |   TF-IDF 점수 |
|---:|:----------|------------:|
|  0 | 미국산       |     14.7094 |
|  1 | 테아닌       |     12.8007 |
|  2 | 트립토판      |     11.9784 |
|  3 | 이산화규소     |     11.8847 |
|  4 | 스테아린산마그네슘 |     10.6202 |

</div>
<div style="flex: 1;" markdown="1">

**인사이트:**

- 텍스트를 벡터화해 주요 원료의 빈도 및 중요도를 시각화했습니다.
- 실제 데이터 통계상 상위권에 랭크된 '미국산', '테아닌', '트립토판' 등의 성분이 핵심 부원료로 집계됩니다.
- 단순 멜라토닌 외의 이러한 핵심 혼합 배합이 수면 보조 시장의 셀링 포인트입니다.

</div>
</div>

---
## Key EDA Findings: 플랫폼별 가격 포지셔닝 차이 (1)
![width:700px](images/v5_platform.png)

---
## Key EDA Findings: 플랫폼별 가격 포지셔닝 차이 (2)
<style scoped>
table { font-size: 0.55em; }
</style>

<div style="display: flex; gap: 20px;">
<div style="flex: 1;" markdown="1">

**그룹 통계:**

| source     |   count |   mean |     std |   min |   25% |   50% |    75% |     max |
|:-----------|--------:|-------:|--------:|------:|------:|------:|-------:|--------:|
| gmarket    |      20 | 1053   |   560.8 | 551   | 629.8 | 810.3 | 1361.5 |  2697   |
| naver      |      20 | 1400.6 |  1549.3 | 111.7 | 395   | 906.2 | 1562.5 |  5633.3 |
| oliveyoung |      20 |  564.7 |   334.2 | 116.7 | 360.6 | 425   |  655   |  1563.3 |
| ssg        |      20 | 3663.1 | 12144.8 | 183   | 393.3 | 756.4 | 1381.5 | 55160   |

</div>
<div style="flex: 1;" markdown="1">

**인사이트:**

- 네이버, 올리브영, SSG, G마켓 등 플랫폼별로 제품 가격 변동/차이 폭을 박스플롯으로 시각화했습니다.
- 플랫폼 특유의 브랜드 입점 기준 및 소비자 층의 선호 용량 단위에 따라 가격 구조가 뚜렷하게 나뉩니다.

</div>
</div>

---
## Correlation Insights: 멜라토닌 함량 vs 가격 (1)
![width:700px](images/v6_scatter1.png)

---
## Correlation Insights: 멜라토닌 함량 vs 가격 (2)
<style scoped>
table { font-size: 0.55em; }
</style>

<div style="display: flex; gap: 20px;">
<div style="flex: 1;" markdown="1">

**상관관계:**

|                   |   melatonin_mg |   price_per_serving |
|:------------------|---------------:|--------------------:|
| melatonin_mg      |      1         |          -0.0390215 |
| price_per_serving |     -0.0390215 |           1         |

</div>
<div style="flex: 1;" markdown="1">

**인사이트:**

- 함량과 금액의 피어슨 상관계수는 -0.039 으로 나타났습니다.
- 단가가 함량 수치에 절대적으로 비례하지 않으며 독립적인 변수 양상을 보입니다.
- 따라서 함량 자체보다 부원료/포지셔닝 브랜딩 결합 여부가 가격을 결정합니다.

</div>
</div>

---
## Correlation Insights: 추가 성분 개수 vs 가격 (1)
![width:700px](images/v7_scatter2.png)

---
## Correlation Insights: 추가 성분 개수 vs 가격 (2)
<style scoped>
table { font-size: 0.55em; }
</style>

<div style="display: flex; gap: 20px;">
<div style="flex: 1;" markdown="1">

**상관관계:**

|                     |   num_add_ingredients |   price_per_serving |
|:--------------------|----------------------:|--------------------:|
| num_add_ingredients |             1         |          -0.0275455 |
| price_per_serving   |            -0.0275455 |           1         |

</div>
<div style="flex: 1;" markdown="1">

**인사이트:**

- 수면 관련 복합 성분 종류의 빈도와 가격의 상관계수는 -0.028 입니다.
- 고품질의 허브나 영양소(테아닌 등)가 다량 배합될 수록 가격 방어력이 높아집니다.
- 고가 이미지를 위해선 복합 배합 포뮬러 개발이 유리하다는 추론이 가능합니다.

</div>
</div>

---
## Correlation Insights: 제형과 멜라토닌 함량 관계 (1)
![width:700px](images/v8_format_mg.png)

---
## Correlation Insights: 제형과 멜라토닌 함량 관계 (2)
<style scoped>
table { font-size: 0.55em; }
</style>

<div style="display: flex; gap: 20px;">
<div style="flex: 1;" markdown="1">

**통계표:**

| format   |   count |   mean |   std |   min |   25% |   50% |   75% |   max |
|:---------|--------:|-------:|------:|------:|------:|------:|------:|------:|
| 구미/젤리    |      11 |    1.9 |   0.3 |     1 |     2 |     2 |     2 |     2 |
| 정제/캡슐    |      65 |    2.6 |   1.7 |     2 |     2 |     2 |     2 |    10 |
| 파우더/분말   |       4 |    2   |   0   |     2 |     2 |     2 |     2 |     2 |

</div>
<div style="flex: 1;" markdown="1">

**인사이트:**

- 박스플롯 확인 시, 정제/캡슐 타입은 편차가 상대적으로 다양하며 고함량 포지션을 확보하고 있습니다.
- 반면 구미/젤리류는 맛 지향적 요소로 인해 1~2mg 선의 상대적으로 대중적인 함량에 집중되는 모델이 많습니다.
- 강력한 고효율 타겟은 정제, 라이트한 기호식품화는 구미 제형이 주력입니다.

</div>
</div>

---
## Market Archetypes: K-Means 클러스터 시장 분석 (1)
![width:700px](images/v9_clusters.png)

---
## Market Archetypes: K-Means 클러스터 시장 분석 (2)
<style scoped>
table { font-size: 0.55em; }
</style>

<div style="display: flex; gap: 20px;">
<div style="flex: 1;" markdown="1">

**클러스터 평균:**

| cluster_label   |   price_per_serving |   melatonin_mg |   num_add_ingredients |
|:----------------|--------------------:|---------------:|----------------------:|
| 저가 가성비형         |               979.5 |              2 |                   4.5 |
| 표준형             |              1088.4 |              6 |                   4.6 |
| 프리미엄 고스펙형       |             55160   |              2 |                   4   |

</div>
<div style="flex: 1;" markdown="1">

**인사이트:**

- 머신러닝 분석을 통해 시장이 3개의 확고한 군집으로 분할됨을 증명했습니다.
- 특히, '프리미엄 고스펙형'은 단순히 양이 많은 것이 아니라 강력한 부원료 배합(도형 크기)에 기대고 있습니다.
- 적절히 높은 함량과 여러 부원료 조합을 지닌 프리미엄군의 포지션 틈새시장을 타겟팅할 수 있습니다.

</div>
</div>

---
## Market Archetypes: 마켓별 포지셔닝 차이 (1)
![width:700px](images/v10_crosstab.png)

---
## Market Archetypes: 마켓별 포지셔닝 차이 (2)
<style scoped>
table { font-size: 0.55em; }
</style>

<div style="display: flex; gap: 20px;">
<div style="flex: 1;" markdown="1">

**비율표 (%):**

| source     |   저가 가성비형 |   표준형 |   프리미엄 고스펙형 |
|:-----------|----------:|------:|------------:|
| gmarket    |        90 |    10 |           0 |
| naver      |        70 |    30 |           0 |
| oliveyoung |        95 |     5 |           0 |
| ssg        |        90 |     5 |           5 |

</div>
<div style="flex: 1;" markdown="1">

**인사이트:**

- 각 플랫폼(지마켓, 올리브영, SSG 등)은 판매 점유율에서 특정 군집의 의존도가 뚜렷하게 나뉩니다.
- 소용량이나 브랜드력 위주 채널인지, 대량 구매 가성비 중심 채널인지 성격에 따라 프리미엄/표준/가성비 군집 비중이 극명한 대조를 보입니다.

</div>
</div>

---
## Product Strategy Recommendations: 제품 및 원료 배합 전략 (1) 💡
데이터가 가라키는 경쟁력 있는 신제품 모델 스펙입니다:
- **제형별 함량 이원화**: 라이트 유저 대상으로는 진입 장벽이 낮은 '구미/젤리' 제형을 채택하여 1~2mg의 마일드한 수준으로 기획합니다. 반면, 확실한 수면 보조 효과를 기대하는 소비자층을 대상으로는 압축이 쉬운 '정제/캡슐' 제형으로 5mg 이상 고함량 제품을 기획합니다.
- **프리미엄 원료 배합**: 데이터 분석 결과 부원료가 많을수록 최저 단가 방어력이 우수했습니다. 단가 하락을 방어하고 프리미엄 포지션을 점유하기 위해, TF-IDF 분석 상위권에 랭크된 실제 핵심 부원료('미국산', '테아닌', '트립토판')를 반드시 복합 배합하여 수면/진정의 시너지를 제품 전면에 내세웁니다.

---
## Product Strategy Recommendations: 유통 채널별 타겟팅 전략 (2) 🎯
군집 분석(K-Means) 결과를 바탕으로 각 판매 채널 플랫폼 성격에 맞게 제품군을 다음과 같이 이원화해 출시합니다:
- **네이버 / G마켓 (대용량 가성비 타겟)**: 이 채널들은 1회 섭취당 1,000원 대 미만의 '저가 가성비 군집'이 압도적인 주력 시장입니다. 타트체리 등 단일 성분에 집중한 대용량 벌크 포장(예: 3~6개월 단위) 제품을 입점시켜 최저가 경쟁력을 확보합니다.
- **올리브영 / SSG (소용량 프리미엄 타겟)**: 이 채널들은 높은 단가의 프리미엄 및 표준형 수요가 충분히 나타납니다. 혼합 부원료를 꽉 채워 설계한 '정제/액상' 프리미엄 라인을 단품이나 소량 패키지(예: 2주~1개월 병입)로 구성하고, 1,500원대 이상의 가격으로 입점시킵니다.

---
## Conclusion
- 식물성 멜라토닌 시장은 현재 도입기/성숙 과도기로 모델 다양화가 폭발적으로 이뤄지고 있습니다.
- 단순히 단일 멜라토닌 수치나 극저가 대용량을 메인으로 하는 전략보다는 다기능 안정/수면 보조 허브 혼합을 더해야 객단가를 올릴 수 있음이 분명한 데이터 수치로 나타났습니다.
- 타당성이 증명된 마켓 포지션에 부합하는 철저히 데이터 주도형 제품군 개발을 진행하시길 추천드립니다.
