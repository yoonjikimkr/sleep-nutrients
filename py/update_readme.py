import subprocess
import os
import re

def run_script(script_name):
    result = subprocess.run(["python3", script_name], capture_output=True, text=True)
    return result.stdout

def linkify_output(text):
    # 절대 경로를 상대 경로로 변환
    base_dir = "/Users/kimyo/Documents/PARA/sleep-nutrients/"
    text = text.replace(base_dir, "")
    
    # 텍스트 내의 data/xxx.png 또는 data/xxx.csv 패턴을 마크다운 링크로 변환
    def replacer(match):
        filepath = match.group(0)
        filename = os.path.basename(filepath)
        return f"[{filename}]({filepath})"
    
    # data/ 폴더 내 파일 경로 링크화
    linked_text = re.sub(r'data/[a-zA-Z0-9_\-]+\.(png|csv)', replacer, text)
    return linked_text

readme_header_template = """# 🌙 Sleep Nutrients Project

글로벌(iHerb) 및 국내(Naver) 데이터를 통합 분석하여, 최적의 수면 영양제 복합제 기획과 시장 전략을 수립하는 프로젝트입니다.

---

## 📑 목차 (Table of Contents)
1. [📊 글로벌 성분 단순 등장 빈도 (Simple Frequency)](#1--글로벌-성분-단순-등장-빈도-simple-frequency-pyanalyze_cooccurrencepy-실행-결과)
2. [🧮 3040 타겟 성분 짝꿍 확률 매트릭스 (Advanced)](#2-3040-타겟-성분-짝꿍-확률-매트릭스-advanced-pyanalyze_cooccurrence_advancedpy-실행-결과)
3. [🎯 3040 한국 직장인 심층 분석 (Keyword vs Ingredient)](#3-3040-한국-직장인-심층-분석-keyword-vs-ingredient-pyanalyze_3040_strategypy-실행-결과)
4. [🎯 3040 직장인 타겟 고도화 EDA 결과](#4-3040-직장인-타겟-고도화-eda-결과-pyanalyze_3040_strategy_v2py-실행-결과)
5. [🧪 iHerb & Naver 성분 교집합 분석](#5--iherb--naver-성분-교집합-분석-pyanalyze_ingredient_crosspy-실행-결과)
6. [🛡️ 공공데이터 안전성(부작용) 검증 Plan](#6-️-공공데이터-안전성부작용-검증-plan-pyvalidate_safetypy-실행-결과)
7. [🤖 마케팅 머신러닝(ML) 종합 전략 전문](#7--마케팅-머신러닝ml-종합-전략-전문)
8. [📂 리포트 및 소스코드](#8--리포트-및-소스코드-collaboration)
9. [📊 네이버 쇼핑 3040 시장 분석 및 EDA 리포트](#네이버-쇼핑을-활용한-3040세대-수면-영양제-시장-분석-및-eda-리포트)

---

## 1. 📊 글로벌 성분 단순 등장 빈도 (Simple Frequency) (`py/analyze_cooccurrence.py` 실행 결과)

{out_freq}

**[주요 빈도 분석 차트]**
![성분 등장 빈도](data/chart_true_ingredient_frequency.png)

---

## 2. 🧮 3040 타겟 성분 짝꿍 확률 매트릭스 (Advanced) (`py/analyze_cooccurrence_advanced.py` 실행 결과)

```text
{out3}
```

**[짝꿍 확률 히트맵]**
- ![통합 히트맵](data/chart_cooccurrence_heatmap_combined.png)
- ![iHerb 히트맵](data/chart_cooccurrence_heatmap_iherb.png)
- ![Naver 히트맵](data/chart_cooccurrence_heatmap_naver.png)

---

## 3. 🎯 3040 한국 직장인 심층 분석 (Keyword vs Ingredient) (`py/analyze_3040_strategy.py` 실행 결과)

{out1}

**[3040 타겟 성분 조합 분석]**
![3040 성분 짝꿍](data/chart_3040_ingredient_pairs.png)

---

## 4. 🎯 3040 직장인 타겟 고도화 EDA 결과 (`py/analyze_3040_strategy_v2.py` 실행 결과)

{out2}

---

## 5. 🧪 iHerb & Naver 성분 교집합 분석 (`py/analyze_ingredient_cross.py` 실행 결과)

{out_cross}

---

## 6. 🛡️ 공공데이터 안전성(부작용) 검증 Plan (`py/validate_safety.py` 실행 결과)

```text
{out4}
```

---

## 7. 🤖 마케팅 머신러닝(ML) 종합 전략 전문

{marketing_strategy}

---

## 8. 📂 리포트 및 소스코드 (Collaboration)

- **분석 보고서 (마크다운 문서)**
  - [`md/3040_marketing_ml_strategy.md`](md/3040_marketing_ml_strategy.md): 3040 타겟 배합 및 마케팅 ML 전략
  - [`md/sleep_supplement_strategy_report.md`](md/sleep_supplement_strategy_report.md): 수면 영양제 시장 전략 리포트

- **분석 스크립트 (Python)**
  - [`py/analyze_3040_strategy.py`](py/analyze_3040_strategy.py): 키워드 vs 성분 성과 비교
  - [`py/analyze_cooccurrence.py`](py/analyze_cooccurrence.py): 성분별 단순 빈도 분석
  - [`py/analyze_cooccurrence_advanced.py`](py/analyze_cooccurrence_advanced.py): 성분 간 조합 확률(%) 분석
  - [`py/validate_safety.py`](py/validate_safety.py): 공공데이터 기반 안전성 가이드
"""

if __name__ == "__main__":
    out_freq = linkify_output(run_script("py/analyze_cooccurrence.py"))
    out1 = linkify_output(run_script("py/analyze_3040_strategy.py"))
    out2 = linkify_output(run_script("py/analyze_3040_strategy_v2.py"))
    out3 = linkify_output(run_script("py/analyze_cooccurrence_advanced.py"))
    out_cross = linkify_output(run_script("py/analyze_ingredient_cross.py"))
    out4 = linkify_output(run_script("py/validate_safety.py"))
    
    # 마케팅 전략 전문 로드
    marketing_strategy = ""
    try:
        with open("md/3040_marketing_ml_strategy.md", "r", encoding="utf-8") as f:
            marketing_strategy = f.read()
    except:
        marketing_strategy = "마케팅 전략 파일을 찾을 수 없습니다."
    
    # 다른 작업자 원본 보존 로직
    existing_content = ""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            existing_content = f.read()
    except:
        pass
        
    keyword = "# 네이버 쇼핑을 활용한 3040세대 수면 영양제 시장 분석 및 EDA 리포트"
    preserved_bottom = ""
    if keyword in existing_content:
        preserved_bottom = keyword + existing_content.split(keyword)[1]
        
    final_content = readme_header_template.format(
        out_freq=out_freq, out1=out1, out2=out2, out3=out3, out_cross=out_cross, out4=out4,
        marketing_strategy=marketing_strategy
    ) + "\n\n" + preserved_bottom
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(final_content)
    print("README.md updated with full strategy and markdown tables!")
    

