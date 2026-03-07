# 쇼핑 검색 API 개요 및 레퍼런스

네이버 검색의 쇼핑 검색 결과를 반환하는 API입니다.

## 1. 개요
- **기능**: 쇼핑 검색 결과를 XML 또는 JSON 형식으로 반환.
- **인증 방식**: 비로그인 방식.

## 2. 쇼핑 검색 결과 조회
- **요청 URL**: 
    - `https://openapi.naver.com/v1/search/shop.json` (JSON)
    - `https://openapi.naver.com/v1/search/shop.xml` (XML)
- **HTTP 메서드**: `GET`
- **주요 파라미터**:
    - `query`: 검색어 (UTF-8 인코딩)
    - `display`: 한 번에 표시할 검색 결과 개수 (1~100)
    - `start`: 검색 시작 위치 (1~1000)
    - `sort`: `sim`(유사도순), `date`(날짜순), `asc`(가격오름차순), `dsc`(가격내림차순)

## 3. 요청 예시 (curl)
```bash
curl "https://openapi.naver.com/v1/search/shop.json?query=주식&display=10&start=1&sort=sim" \
    -H "X-Naver-Client-Id: {CLIENT_ID}" \
    -H "X-Naver-Client-Secret: {CLIENT_SECRET}"
```

## 4. 참고
쇼핑 검색 상세 구현은 블로그 검색 구현 방식과 유사합니다. 상세한 응답 필드와 상품군 타입 정의는 개발자 센터를 참고하시기 바랍니다.
