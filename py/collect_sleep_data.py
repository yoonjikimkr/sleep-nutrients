import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

CLIENT_ID = os.getenv('NAVER_CLIENT_ID').strip()
CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET').strip()

HEADERS = {
    'X-Naver-Client-Id': CLIENT_ID,
    'X-Naver-Client-Secret': CLIENT_SECRET,
    'Content-Type': 'application/json'
}

def get_search_trend(keyword_groups, start_date, end_date):
    """네이버 데이터랩 통합 검색어 트렌드 수집 (5년)"""
    url = "https://openapi.naver.com/v1/datalab/search"
    
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "date",
        "keywordGroups": keyword_groups,
        "device": "",
        "gender": "",
        "ages": []
    }
    
    print(f"--- 통합 검색어 트렌드 요청: {start_date} ~ {end_date} ---")
    response = requests.post(url, headers=HEADERS, data=json.dumps(body, ensure_ascii=False).encode('utf-8'))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def get_search_results(query, target="blog"):
    """네이버 검색 API (블로그/쇼핑) 수집"""
    url_map = {
        "blog": "https://openapi.naver.com/v1/search/blog.json",
        "shop": "https://openapi.naver.com/v1/search/shop.json"
    }
    url = f"{url_map[target]}?query={query}&display=100"
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

def get_shopping_insight_trend(category_id, keywords):
    """네이버 쇼핑인사이트 키워드별 트렌드 수집"""
    url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365) # 쇼핑인사이트는 보통 1년 단위
    
    keyword_list = [{"name": kw, "param": [kw]} for kw in keywords]
    
    body = {
        "startDate": start_date.strftime('%Y-%m-%d'),
        "endDate": end_date.strftime('%Y-%m-%d'),
        "timeUnit": "date",
        "category": category_id,
        "keyword": keyword_list,
        "device": "",
        "gender": "",
        "ages": []
    }
    
    response = requests.post(url, headers=HEADERS, data=json.dumps(body, ensure_ascii=False).encode('utf-8'))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def main():
    # 1. 환경 설정
    base_dir = "data"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    keywords = ["불면", "잠이 안 와", "수면 영양제", "멜라토닌"]
    keyword_groups = [{"groupName": kw, "keywords": [kw]} for kw in keywords]
    
    # 2. 통합 검색어 트렌드 수집
    # 과거 (2016-01-01 ~ 2020-12-31)
    past_trend = get_search_trend(keyword_groups, "2016-01-01", "2020-12-31")
    if past_trend:
        with open(f"{base_dir}/search_trend_past.json", "w", encoding="utf-8") as f:
            json.dump(past_trend, f, ensure_ascii=False, indent=4)
        print(f"Saved: {base_dir}/search_trend_past.json")

    # 현재 (2021-01-01 ~ 현재)
    end_dt = datetime.now()
    present_trend = get_search_trend(keyword_groups, "2021-01-01", end_dt.strftime('%Y-%m-%d'))
    if present_trend:
        with open(f"{base_dir}/search_trend_present.json", "w", encoding="utf-8") as f:
            json.dump(present_trend, f, ensure_ascii=False, indent=4)
        print(f"Saved: {base_dir}/search_trend_present.json")

    # 3. 블로그 및 쇼핑 검색 결과 (기초 데이터는 현재 기준 유지)
    for kw in keywords:
        print(f"--- 키워드 수집: {kw} ---")
        blogs = get_search_results(kw, "blog")
        if blogs:
            df_blog = pd.DataFrame(blogs)
            df_blog.to_csv(f"{base_dir}/blog_{kw}.csv", index=False, encoding='utf-8-sig')
            
        shops = get_search_results(kw, "shop")
        if shops:
            df_shop = pd.DataFrame(shops)
            df_shop.to_csv(f"{base_dir}/shop_{kw}.csv", index=False, encoding='utf-8-sig')

    # 4. 쇼핑인사이트 키워드 트렌드
    shopping_trend = get_shopping_insight_trend("50000030", ["수면 영양제", "멜라토닌"])
    if shopping_trend:
        with open(f"{base_dir}/shopping_insight_trend.json", "w", encoding="utf-8") as f:
            json.dump(shopping_trend, f, ensure_ascii=False, indent=4)
        print(f"Saved: {base_dir}/shopping_insight_trend.json")

if __name__ == "__main__":
    main()
