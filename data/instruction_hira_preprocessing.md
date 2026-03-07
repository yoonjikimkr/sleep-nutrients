# HIRA 데이터 전처리 작업 지시서 (instruction_hira_preprocessing.md)

이 지시서는 `docs/hira_data_schema.md`의 분석 결과를 바탕으로, 수면 장애(F51) 엑셀 데이터를 마케팅 분석이 가능한 통합 데이터셋으로 정제하기 위한 가이드를 제공합니다.

## 0. 예상 파일 트리 구조
작업 수행 시 `sleep` 폴더의 구조는 다음과 같아야 합니다.
```text
sleep/
├── docs/
│   ├── hira_data_schema.md               # 데이터 구조 분석서
│   └── instruction_hira_preprocessing.md  # [본 파일] 전처리 작업 지시서
├── sleep1.xlsx                           # 연령대별 비용 데이터
├── sleep2.xlsx                           # 연령대별 성별 인원 데이터
├── sleep3.xlsx                           # 상세 로우 데이터 (연도/성별/연령 등)
├── chart.xlsx                            # 요약 그래프 (분석 제외)
├── analyze_data.py                       # 데이터 분석 스크립트
├── preprocess.py                         # [작성 필요] 전처리 실행 스크립트
└── f51_target_merged.csv                 # [결과물] 최종 정제 통합 데이터
```

## 1. 대상 파일 및 로드 아키텍처
- **대상**: `sleep1.xlsx`, `sleep2.xlsx`, `sleep3.xlsx`
- **로직**: `glob` 또는 리스트 반복문을 사용하여 파일을 순차적으로 읽고, 각 `DataFrame`을 리스트에 담아 최종적으로 `pd.concat()`을 수행함.

---

## 2. 세부 정제 단계 (Cleanup Logistics)

### STEP 1: 불필요한 메타 행 제거
- 심평원 데이터 상단의 설명용 행(일반적으로 1~3행)을 로드 시점에 제외함.
- `pd.read_excel(file, skiprows=3)`와 같이 설정하여 실제 컬럼명이 나타나는 행부터 데이터를 읽음.

### STEP 2: '총개/계' 행 제외 및 컬럼 정리
- 특정 컬럼(예: '성별' 또는 '연령대')에 '계', '총계'라고 명시된 행은 분석 시 중복 집계를 유발하므로 필터링하여 제거함.
  ```python
  df = df[~df['성별'].str.contains('계', na=False)]
  ```

### STEP 3: 데이터 타입 정규화 (Comma 처리)
- 수치 데이터에 포함된 콤마(`,`)를 제거하고 실수형(float) 또는 정수형(int)으로 변환함.
  ```python
  df[col] = df[col].replace({',': ''}, regex=True).astype(float)
  ```

---

## 3. 데이터 구조 재배치 (Reshaping)

### 3.1 Pivot/Melt 전략
각 파일의 지표(진료비, 환자수 등)를 '연도'와 '성별'이라는 기준 차원으로 재정렬함.
- **Melt**: 가로로 나열된 연도별 지표를 세로로 길게 변환하여 BI 도구나 분석용 스크립트에서 활용하기 좋게 만듦.
  - `id_vars=['성별', '연령대']`
  - `value_vars=['2021년_비용', '2022년_비용', ...]`
- **Pivot Table**: 최종 병합 후, 마케팅 타겟팅을 위해 `index=['연령대']`, `columns=['성별']` 형태로 요약함.

---

## 4. 최종 통합 파일 사양
- **파일명**: `f51_target_merged.csv`
- **인코딩**: `utf-8-sig` (Excel 호환성 고려)
- **결측값 처리**: 수치형 데이터의 `NaN`은 `0`으로 일관되게 채움.

---

## 5. 작업 체크리스트
- [ ] 파일 로드 시 `openpyxl` 엔진을 명시했는가?
- [ ] 상단 3~4개의 Empty/Meta 행이 제거되었는가?
- [ ] '성별' 컬럼에 '계' 데이터가 없는지 확인했는가?
- [ ] 모든 수치 컬럼에서 `,`가 제거되고 `Numeric` 타입으로 변환되었는가?
- [ ] `Melt`를 통해 '연도' 컬럼이 변수로 생성되었는가?
- [ ] 최종 결과물이 `f51_target_merged.csv`로 저장되는가?
