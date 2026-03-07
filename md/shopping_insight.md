# 쇼핑인사이트 API 개요 및 레퍼런스

쇼핑인사이트 API는 네이버 데이터랩의 쇼핑 데이터를 RESTful 형식으로 제공합니다.

## 1. API 개요
- **기능**: 네이버 통합검색 쇼핑 영역 및 네이버쇼핑 검색 클릭 추이 데이터 반환.
- **호출 한도**: 하루 1,000회.
- **인증 방식**: 비로그인 방식 (Client ID/Secret 필요).

## 2. 분야별 트렌드 조회
- **요청 URL**: `https://openapi.naver.com/v1/datalab/shopping/categories`
- **HTTP 메서드**: `POST`
- **주요 파라미터 (JSON)**:
    - `startDate`: 시작일 (YYYY-MM-DD)
    - `endDate`: 종료일 (YYYY-MM-DD)
    - `timeUnit`: `date`, `week`, `month`
    - `category`: 분야 이름과 `cat_id` 리스트
    - `device`, `gender`, `ages`: 필터 조건

## 3. Python 구현 예제
```python
import os
import sys
import urllib.request
import json

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
url = "https://openapi.naver.com/v1/datalab/shopping/categories"

body = {
    "startDate": "2023-01-01",
    "endDate": "2023-12-31",
    "timeUnit": "month",
    "category": [{"name": "패션의류", "param": ["50000000"]}],
    "device": "pc",
    "ages": ["20", "30"],
    "gender": "f"
}

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
request.add_header("Content-Type", "application/json")

response = urllib.request.urlopen(request, data=json.dumps(body).encode("utf-8"))
if response.getcode() == 200:
    print(response.read().decode('utf-8'))
else:
    print("Error Code:" + str(response.getcode()))
```
