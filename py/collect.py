import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import time

# 1. 환경 설정 및 API 라이브러리 로드
# 현재 폴더의 .env 파일을 로드합니다.
load_dotenv(dotenv_path=".env")
CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')

def get_headers():
    return {
        'X-Naver-Client-Id': CLIENT_ID,
        'X-Naver-Client-Secret': CLIENT_SECRET,
        'Content-Type': 'application/json'
    }

def search_shopping(query, display=100, start=1):
    """
    네이버 쇼핑 검색 API를 호출합니다.
    """
    url = "https://openapi.naver.com/v1/search/shop.json"
    params = {
        'query': query,
        'display': display,
        'start': start,
        'sort': 'sim' # 유사도순 (기본값)
    }
    
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error for query '{query}': {response.status_code}")
        print(response.text)
        return None

def collect_data():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("API 인증 정보를 찾을 수 없습니다. .env 파일을 확인하세요.")
        return

    keywords = ["수면 영양제", "숙면 영양제", "멜라토닌", "수면 보조제", "잠 영양제"]
    all_items = []
    
    # 각 키워드별로 최대 1000개 수집 가능 (API 제약)
    # 여기서는 효율성을 위해 각 키워드별 상위 200개씩 총 1000개 수준으로 수집
    for kw in keywords:
        print(f"Searching for '{kw}'...")
        for start in range(1, 201, 100):
            result = search_shopping(kw, display=100, start=start)
            if result and 'items' in result:
                items = result['items']
                for item in items:
                    # 키워드 정보 추가
                    item['search_keyword'] = kw
                all_items.extend(items)
            time.sleep(0.1) # API Rate Limit 방지

    df = pd.DataFrame(all_items)
    
    if df.empty:
        print("수집된 데이터가 없습니다.")
        return

    # 중복 제거 (productId 기준)
    df = df.drop_duplicates(subset=['productId'])
    
    # 카테고리 필터링: 사용자 요청 카테고리 ID 2|50000023 (식품 > 건강식품 > 영양제 > 수면/신경안정)
    # API에서는 category1-4 텍스트로 오므로, 건강식품/영양제 키워드 포함 여부로 1차 필터링
    # (실제 카테고리 ID 매칭은 검색 결과의 링크나 상세 정보가 필요하지만, 
    # API 결과의 category3/4가 '영양제'나 '수면' 관련인지 확인)
    
    print(f"Total unique items before filtering: {len(df)}")
    if not df.empty:
        print("Sample categories found:")
        print(df[['category2', 'category3', 'category4']].drop_duplicates().head(10))
    
    # 필터링 조건: 
    # 1. category2 가 '건강식품' 이거나
    # 2. category3 가 '영양제' 이거나
    # 3. title에 '영양제', '보조제', '수면', '숙면', '잠', '멜라토닌' 등 키워드 포함
    
    mask = (
        df['category2'].str.contains('건강식품', na=False) |
        df['category3'].str.contains('영양제', na=False) |
        df['title'].str.contains('수면|숙면|잠|영양제|보조제|멜라토닌', na=False)
    )
    df_filtered = df[mask].copy()
    
    print(f"Total items after filtering: {len(df_filtered)}")
    
    # 데이터 저장
    os.makedirs("data", exist_ok=True)
    filename = "data/sleep_supplements.csv"
    df_filtered.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Saved {len(df_filtered)} items to {filename}")

if __name__ == "__main__":
    collect_data()
