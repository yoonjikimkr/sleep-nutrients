import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
import time

# 1. 환경 설정 및 API 라이브러리 로드
load_dotenv(dotenv_path=".env")
CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')

def get_headers():
    return {
        'X-Naver-Client-Id': CLIENT_ID,
        'X-Naver-Client-Secret': CLIENT_SECRET,
        'Content-Type': 'application/json'
    }

def get_datalab_search(keyword_groups, start_date, end_date, device="", gender="", ages=[]):
    """
    네이버 통합 검색어 트렌드 API를 호출합니다.
    """
    url = "https://openapi.naver.com/v1/datalab/search"
    
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "month",
        "keywordGroups": keyword_groups,
        "device": device,
        "gender": gender,
        "ages": ages
    }
    
    response = requests.post(url, headers=get_headers(), data=json.dumps(body, ensure_ascii=False).encode('utf-8'))
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"API Error: {response.status_code}")
        print(response.text)
        return None

def collect_trends():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("API 인증 정보를 찾을 수 없습니다. .env 파일을 확인하세요.")
        return

    # 키워드 그룹 정의 (유형별)
    # 1. 증상/고민형
    # 2. 해결책형
    # 3. 성분형 (주요 5종)
    keyword_groups = [
        {"groupName": "증상_불면증", "keywords": ["불면증", "수면장애", "잠이 안와요"]},
        {"groupName": "고민_깊은잠", "keywords": ["깊은잠", "숙면", "수면무호흡", "코골이"]},
        {"groupName": "해결_영양제", "keywords": ["수면 영양제", "수면 보조제", "슬립토닌"]},
        {"groupName": "성분_멜라토닌", "keywords": ["멜라토닌", "식물성 멜라토닌"]},
        {"groupName": "성분_테아닌_마그네슘", "keywords": ["L-테아닌", "테아닌", "마그네슘"]}
    ]

    start_date = "2024-01-01"
    end_date = "2025-12-31"

    # 전체 트렌드 수집
    print("수집 중: 전체 트렌드...")
    res_all = get_datalab_search(keyword_groups, start_date, end_date)
    
    # 인구통계 데이터 수집 (성별)
    print("수집 중: 성별 트렌드 (여성)...")
    res_female = get_datalab_search(keyword_groups, start_date, end_date, gender="f")
    print("수집 중: 성별 트렌드 (남성)...")
    res_male = get_datalab_search(keyword_groups, start_date, end_date, gender="m")

    # 인구통계 데이터 수집 (연령대)
    # ages: 1:0~12, 2:13~18, 3:19~24, 4:25~29, 5:30~34, 6:35~39, 7:40~44, 8:45~49, 9:50~54, 10:55~59, 11:60~
    age_groups = {
        "20대": ["3", "4"],
        "30대": ["5", "6"],
        "40대": ["7", "8"],
        "50대이상": ["9", "10", "11"]
    }
    
    age_results = {}
    for label, ages in age_groups.items():
        print(f"수집 중: 연령별 트렌드 ({label})...")
        age_results[label] = get_datalab_search(keyword_groups, start_date, end_date, ages=ages)
        time.sleep(0.5)

    # 데이터 가공 및 저장
    rows = []
    
    def extract_data(res, label_type, label_val):
        if not res or 'results' not in res: return
        for group in res['results']:
            group_name = group['title']
            for data in group['data']:
                rows.append({
                    'period': data['period'],
                    'group': group_name,
                    'ratio': data['ratio'],
                    'type': label_type,
                    'value': label_val
                })

    extract_data(res_all, 'total', 'all')
    extract_data(res_female, 'gender', 'female')
    extract_data(res_male, 'gender', 'male')
    for label, res in age_results.items():
        extract_data(res, 'age', label)

    df = pd.DataFrame(rows)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/search_trends.csv", index=False, encoding='utf-8-sig')
    print(f"데이터 저장 완료: data/search_trends.csv (총 {len(df)}행)")

if __name__ == "__main__":
    collect_trends()
