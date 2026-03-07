import pandas as pd
import os

# 페르소나 정의 및 니즈 맵
PERSONA_NEEDS = {
    'Office Worker (심야 퇴근형)': {
        'needs': ['스트레스 완화', '빠른 입면', '뇌 전원 끄기'],
        'base_ings': ['Magnesium Glycinate', 'L-Theanine'],
        'boost_ings': ['Tryptophan'],
        'marketing_hook': '오늘 하루의 긴장을 끄고, 5분 만에 딥슬립으로 안내합니다.'
    },
    'Elderly (중장년층 유지가 힘든형)': {
        'needs': ['수면 유지', '중도 각성 방지', '근육 이완'],
        'base_ings': ['Magnesium Taurate', 'Glycine'],
        'boost_ings': ['Tart Cherry'],
        'marketing_hook': '자다 깨지 않는 아침, 개운한 통잠의 기쁨을 선사합니다.'
    },
    'Junior (시험/숏폼 중독형)': {
        'needs': ['도파민 정화', '심신 안정', '디지털 디톡스 수면'],
        'base_ings': ['GABA', 'Lemon Balm'],
        'boost_ings': ['Chamomile'],
        'marketing_hook': '각성된 뇌를 차분하게, 가장 순수한 자연의 휴식을 선물하세요.'
    }
}

def recommend_formulation(persona_key=None):
    print("--- 마케팅 기반 최적 성분 추천 시스템 ---")
    
    if not persona_key:
        # 모든 페르소나 결과 출력
        for target, data in PERSONA_NEEDS.items():
            print(f"\n🎯 타겟: {target}")
            print(f"✅ 추천 배합: {', '.join(data['base_ings'])} + {', '.join(data['boost_ings'])}")
            print(f"💡 마케팅 소구점: {data['marketing_hook']}")
            print(f"🔍 핵심 니즈: {', '.join(data['needs'])}")
    else:
        # 특정 페르소나 추천
        data = PERSONA_NEEDS.get(persona_key)
        if data:
            print(f"\n🎯 타겟: {persona_key}")
            print(f"✅ 추천 배합: {', '.join(data['base_ings'])} + {', '.join(data['boost_ings'])}")
            print(f"💡 마케팅 소구점: {data['marketing_hook']}")
        else:
            print("해당 페르소나 정보를 찾을 수 없습니다.")

if __name__ == "__main__":
    recommend_formulation()
