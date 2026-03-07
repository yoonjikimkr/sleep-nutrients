# 네이버 통합검색어 트렌드 분석 작업지시서 (고도화 버전)

이 문서는 `project-1/docs/`에 저장된 네이버 공식 API 문서를 바탕으로, 특정 주제에 대한 **최근 5년간의 일자별 통합검색 트렌드**를 수집하고 확인하는 과정을 안내합니다.

## 1. 개요
- **API 종류**: 네이버 데이터랩 - 통합검색어 트렌드 (비로그인 방식)
- **분석 목표**: 특정 주제어 그룹에 대한 네이버 내 검색량 변화 추이 분석
- **수집 기간**: 최근 5년 (실행 시점 기준 -1,825일 ~ 현재)
- **데이터 특징**: 절대적인 검색 횟수가 아닌, 기간 내 최대 검색량을 100으로 설정한 **상대적 지표**임

## 2. 사전 준비 (Reference Docs)
- [비로그인 API 공통 가이드](docs/api_guide.md): Client ID/Secret 인증 방식 확인
- [데이터랩 서비스 개요](docs/datalab.md): 검색어 트렌드 데이터의 특성 이해

## 3. API 상세 스펙
- **요청 URL**: `https://openapi.naver.com/v1/datalab/search`
- **HTTP Method**: `POST`
- **인증 헤더**:
  - `X-Naver-Client-Id`: 발급받은 클라이언트 아이디
  - `X-Naver-Client-Secret`: 발급받은 클라이언트 시크릿
  - `Content-Type`: `application/json`

## 4. 데이터 수집 단계 (Step-by-Step)

### 단계 1: 환경 변수 구성
`project-1/.env` 파일에 API 자격 증명을 설정합니다.
```env
NAVER_CLIENT_ID=여러분의_아이디
NAVER_CLIENT_SECRET=여러분의_시크릿
```

### 단계 2: 날짜 계산 및 요청 데이터 구성
네이버 데이터랩 API는 한 번의 요청으로 최대 5년치 데이터를 수집할 수 있습니다. 
- `startDate`: 실행일 기준 5년 전 (예: `2021-02-28`)
- `endDate`: 현재 날짜 (예: `2026-02-28`)
- `timeUnit`: `date` (일간 단위)

### 단계 3: 수집 스크립트 작성 (`collect.py`)
아래 예시 코드를 참고하여 `project-1/collect.py`를 작성합니다.

```python
import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def fetch_search_trend():
    url = "https://openapi.naver.com/v1/datalab/search"
    headers = {
        "X-Naver-Client-Id": os.getenv("NAVER_CLIENT_ID"),
        "X-Naver-Client-Secret": os.getenv("NAVER_CLIENT_SECRET"),
        "Content-Type": "application/json"
    }

    # 5년 전 날짜 계산
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 5)

    body = {
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
        "timeUnit": "date",
        "keywordGroups": [
            {
                "groupName": "인공지능",
                "keywords": ["AI", "ChatGPT", "LLM", "Deep Learning"]
            }
        ],
        "device": "", # 전체
        "ages": [],   # 전체
        "gender": ""  # 전체
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        data = response.json()
        with open("data/trend_results.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("데이터 수집 완료: data/trend_results.json")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    fetch_search_trend()
```

## 5. 데이터 확인 및 검증 절차

### 1) 데이터 무결성 확인
- 수집된 `data/trend_results.json` 파일을 열어 `results` 필드 내 `data` 배열에 실제 일자별 값이 있는지 확인합니다.
- 데이터 포인트의 개수가 약 1,825개(5년 x 365일) 내외인지 확인합니다.

### 2) 상대 지표 검증
- 수집된 데이터 중 `value`가 **100**인 지점이 있는지 확인합니다. (해당 기간 중 검색량이 가장 폭발적이었던 시점입니다.)

### 3) 시각화 확인 (`visualize.py`)
- `pandas`를 사용하여 `data` 내부의 `period`와 `ratio`를 로드합니다.
- `matplotlib`을 활용해 5년간의 추세선을 그립니다. (한글 깨짐 방지를 위해 `koreanize-matplotlib` 사용 필수)

## 6. 주의 사항
- **상대적 값**: 다른 키워드와 비교할 때, 각 키워드 릴리스별로 100의 기준이 다를 수 있음을 인지해야 합니다.
- **API 한도**: 비로그인 방식의 일일 호출 한도를 준수하십시오.
- **데이터 보안**: `.env` 파일이 Git에 업로드되지 않도록 `.gitignore`에 추가하십시오.
