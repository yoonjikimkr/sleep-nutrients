# 네이버 뉴스 기사 수집 및 분석 작업지시서

이 문서는 네이버 검색 API를 활용하여 최근 10년간의 특정 수면 관련 키워드 기사를 수집하고, 사회적 이슈의 변화를 분석하기 위한 가이드입니다.

## 1. 개요
- **API 종류**: 네이버 검색 - 뉴스 (비로그인 방식)
- **수집 키워드**:
    1. `불면 증가`
    2. `멜라토닌 부작용`
    3. `수면제 의존`
- **분석 목표**: 수면 관련 부정적 이슈 및 사회적 현상의 10년간 변화 추이 확인

## 2. API 상세 스펙
- **요청 URL**: `https://openapi.naver.com/v1/search/news.json`
- **HTTP Method**: `GET`
- **주요 파라미터**:
    - `query`: 검색어 (UTF-8 인코딩)
    - `display`: 한 번에 가져올 결과 개수 (최대 100)
    - `start`: 검색 시작 위치 (최대 1000)
    - `sort`: `sim` (유사도순), `date` (날짜순)

## 3. 데이터 수집 전략 (10년치 확보)
네이버 검색 API는 한 호출당 최대 1,000건(display 100 * start 10회)까지만 조회가 가능합니다. 10년간의 데이터를 폭넓게 수집하기 위해 다음과 같은 전략을 사용합니다.

### 전략: 시기별 분할 수집 (옵션)
검색량이 많은 키워드의 경우, `sim`(유사도순)으로 정렬하여 각 키워드별 상위 1,000개의 핵심 기사를 우선 수집하여 질적 분석을 수행합니다. 또는 특정 연도별로 쿼리를 분할(`query="불면 증가 2023"`)하여 양적 수집 범위를 넓힐 수 있습니다.

## 4. 수집 단계 (Step-by-Step)

### 단계 1: 수집 스크립트 작성 (`collect_articles.py`)
아래 코드를 참고하여 기사 제목, 링크, 요약(description), 발행일을 수집합니다.

```python
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def fetch_news(query, display=100, start=1):
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={display}&start={start}&sort=sim"
    headers = {
        "X-Naver-Client-Id": os.getenv("NAVER_CLIENT_ID"),
        "X-Naver-Client-Secret": os.getenv("NAVER_CLIENT_SECRET")
    }
    response = requests.get(url, headers=headers)
    return response.json().get('items', []) if response.status_code == 200 else []

def collect_keyword_articles(keyword):
    all_articles = []
    # 최대 1,000건 수집 (API 제약)
    for i in range(1, 11):
        start = (i-1) * 100 + 1
        items = fetch_news(keyword, start=start)
        all_articles.extend(items)
        if not items: break
    
    df = pd.DataFrame(all_articles)
    df.to_csv(f"data/articles_{keyword}.csv", index=False, encoding='utf-8-sig')
    print(f"[{keyword}] 수집 완료: {len(df)}건")

if __name__ == "__main__":
    keywords = ["불면 증가", "멜라토닌 부작용", "수면제 의존"]
    for kw in keywords:
        collect_keyword_articles(kw)
```

## 5. 확인 및 결과 분석 항목

### 1) 기사 배포 추이 분석
- 수집된 `pubDate`를 연도/월별로 그룹화하여 특정 키워드(예: 멜라토닌 부작용)가 급증한 전후 맥락을 파악합니다.

### 2) 핵심 키워드 클라우드
- 기사 제목 및 요약(`description`)에서 명사 위주의 키워드를 추출하여 당시의 주요 논점(예: 처방전, 해외 직구 등)을 분석합니다.

### 3) 대시보드 연동
- 수집된 CSV 파일을 이전 대시보드(`app.py`)의 새로운 탭에 로드하여, 검색 트렌드 급증(Surge) 시점과 관련 뉴스 기사를 매칭하여 분석합니다.

## 6. 주의 사항
- **HTML 태그 제거**: API 응답 중 `description` 필드에는 `<b>`, `&quot;` 등의 태그가 포함되어 있으므로 정제 과정이 필요합니다.
- **중복 제거**: 동일 기사가 여러 매체에서 송고된 경우 제목을 기준으로 중복을 처리하십시오.
