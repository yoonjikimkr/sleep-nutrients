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

def analyze_2030_public_ml():
    print("🚀 [ML분석] 2030 수면장애 공공데이터 기반 타켓 페르소나 군집 분석 (K-Means)")
    
    if not os.path.exists(HIRA_CSV):
        print(f"❌ 데이터 파일을 찾을 수 없습니다: {HIRA_CSV}")
        return

    df = pd.read_csv(HIRA_CSV)
    
    # 1. 2030 데이터 필터링 (20_29세, 30_39세)
    target_ages = ['20_29세', '30_39세']
    df_target = df[df['연령대'].isin(target_ages)].copy()
    
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
    
    # 4. K-Means 클러스터링 (K=3으로 설정: 경증/중증/고위험군 등)
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

    plt.title('2030 수면장애 페르소나 군집 분석 (환자 수 vs 인당 진료비)', fontsize=15)
    plt.xlabel('환자 수 (진료실원수)')
    plt.ylabel('인당 평균 진료비 (요양급여/환자)')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    chart_path = os.path.join(DATA_DIR, 'chart_2030_persona_clusters.png')
    plt.savefig(chart_path, dpi=300)
    plt.close()
    
    print(f"\n✅ 클러스터링 결과 차트 저장 완료: {chart_path}")
    
    # 7. 인사이트 도출
    print("\n💡 데이터 기반 마케팅 인사이트:")
    for cluster in range(3):
        subset = cluster_summary[cluster_summary['cluster'] == cluster]
        if subset['인당_진료비'].values[0] > cluster_summary['인당_진료비'].mean():
            print(f"- [고관여 집단: Cluster {cluster}] 진료비 지출이 높고 내원 빈도가 잦은 집단입니다. '식물성 멜라토닌'과 같은 고효능 프리미엄 배합의 주 타겟입니다.")
        else:
            print(f"- [잠재 수요 집단: Cluster {cluster}] 환자 수는 많으나 개별 지출이 낮은 집단입니다. 일상적 스트레스 케어용 '테아닌/마그네슘' 조합이 적합한 시장입니다.")

if __name__ == "__main__":
    analyze_2030_public_ml()
