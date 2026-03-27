import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 한글 폰트 설정 (macOS)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
HIRA_CSV = os.path.join(DATA_DIR, "f51_target_merged.csv")

def analyze_4050_public_ml():
    print("🚀 [ML분석] 4050 수면장애 공공데이터 기반 타겟 페르소나 군집 분석 (K-Means)")
    
    if not os.path.exists(HIRA_CSV):
        print(f"❌ 데이터 파일을 찾을 수 없습니다: {HIRA_CSV}")
        return

    df = pd.read_csv(HIRA_CSV)
    
    # 1. 4050 데이터 필터링 (40_49세, 50_59세)
    target_ages = ['40_49세', '50_59세']
    df_target = df[df['연령대'].isin(target_ages)].copy()
    
    print(f"  ✅ 대상 데이터 행 수: {len(df_target)}개 (40_49세, 50_59세)")
    
    # 2. 특징 엔지니어링 (Feature Engineering)
    # 인당 진료비 계산 (중요 지표: 얼마나 심각한 질환인가)
    df_target['인당_진료비'] = df_target['요양급여비용'] / df_target['진료실원수']
    # 인당 내원일수
    df_target['인당_내원일수'] = df_target['내원일수'] / df_target['진료실원수']
    
    # Clustering에 사용할 특성 선택
    features = ['진료실원수', '인당_진료비', '인당_내원일수']
    X = df_target[features]
    
    # 3. 데이터 표준화 (Standardization)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4. K-Means 클러스터링 (K=3으로 설정)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_target['cluster'] = kmeans.fit_predict(X_scaled)
    
    # 5. 군집별 특성 분석
    cluster_summary = df_target.groupby('cluster')[features + ['연령대', '성별']].agg({
        '진료실원수': 'mean',
        '인당_진료비': 'mean',
        '인당_내원일수': 'mean',
        '연령대': lambda x: x.mode()[0],
        '성별': lambda x: x.mode()[0]
    }).reset_index()
    
    print("\n📊 군집별 분석 요약:")
    print(cluster_summary.to_markdown(index=False))
    
    # 6. 시각화 (Scatter Plot)
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df_target, x='진료실원수', y='인당_진료비', hue='cluster', size='인당_내원일수', palette='viridis', sizes=(50, 400))
    
    for i in range(len(cluster_summary)):
        plt.annotate(f"Persona {i}", 
                     (cluster_summary.loc[i, '진료실원수'], cluster_summary.loc[i, '인당_진료비']),
                     textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold')

    plt.title('4050 수면장애 페르소나 군집 분석 (환자 수 vs 인당 진료비)', fontsize=15)
    plt.xlabel('환자 수 (진료실원수)')
    plt.ylabel('인당 평균 진료비 (요양급여/환자)')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    chart_path = os.path.join(DATA_DIR, 'chart_4050_persona_clusters.png')
    plt.savefig(chart_path, dpi=300)
    plt.close()
    
    print(f"\n✅ 클러스터링 결과 차트 저장 완료: {chart_path}")
    
    # 7. 인사이트 도출
    print("\n💡 4050 타겟 마케팅 인사이트:")
    for _, row in cluster_summary.iterrows():
        cluster = row['cluster']
        age = row['연령대']
        gender = row['성별']
        cost = row['인당_진료비']
        pats = row['진료실원수']
        if cost > cluster_summary['인당_진료비'].mean():
            print(f"- [고관여 집단: Cluster {cluster}] {age}/{gender} - 진료비 지출이 높음.")
            print(f"  👉 프리미엄 성분(멜라토닌 프리, 아슈와간다+마그네슘) 고단가 전략 타겟.")
        else:
            print(f"- [주류 집단: Cluster {cluster}] {age}/{gender} - 환자수 많고 지속적 방문.")
            print(f"  👉 '갱년기 수면 관리', '중년 만성피로' 키워드 복합 솔루션 적합.")

if __name__ == "__main__":
    analyze_4050_public_ml()
