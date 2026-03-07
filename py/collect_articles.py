import os
import requests
import pandas as pd
import re
from dotenv import load_dotenv
from datetime import datetime

# .env 파일 로드
load_dotenv()

CLIENT_ID = os.getenv('NAVER_CLIENT_ID').strip()
CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET').strip()

HEADERS = {
    'X-Naver-Client-Id': CLIENT_ID,
    'X-Naver-Client-Secret': CLIENT_SECRET
}

def clean_html(text):
    """HTML 태그 및 특수문자 제거"""
    if not text:
        return ""
    # 태그 제거
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    # 특수문자 엔티티 변환 (간단히)
    text = text.replace('&quot;', '"').replace('&apos;', "'").replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return text

def fetch_news(query, display=100, start=1):
    """네이버 뉴스 검색 API 호출"""
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={display}&start={start}&sort=sim"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error {response.status_code} for {query}: {response.text}")
        return []

def collect_keyword_articles(keyword):
    """키워드별 최대 1,000건 기사 수집 및 정제"""
    print(f"--- [{keyword}] 뉴스 수집 시작 ---")
    all_articles = []
    
    # 최대 1,000건 수집 (100개씩 10번 호출)
    for i in range(1, 11):
        start = (i - 1) * 100 + 1
        items = fetch_news(keyword, start=start)
        if not items:
            break
        
        # 데이터 정제
        for item in items:
            item['title'] = clean_html(item['title'])
            item['description'] = clean_html(item['description'])
        
        all_articles.extend(items)
        if len(items) < 100:
            break
            
    if not all_articles:
        print(f"[{keyword}] 수집된 기사가 없습니다.")
        return
        
    df = pd.DataFrame(all_articles)
    
    # 데이터 폴더 확인
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    filename = f"{data_dir}/articles_{keyword.replace(' ', '_')}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"[{keyword}] 수집 완료: {len(df)}건 저장됨 -> {filename}")

if __name__ == "__main__":
    keywords = ["불면 증가", "멜라토닌 부작용", "수면제 의존"]
    for kw in keywords:
        collect_keyword_articles(kw)
