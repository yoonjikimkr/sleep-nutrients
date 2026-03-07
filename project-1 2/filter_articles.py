import pandas as pd
import os
import glob

def filter_articles():
    articles_dir = "/Users/juns/Desktop/fcicb7/project-1/articles"
    target_files = glob.glob(os.path.join(articles_dir, "*.csv"))
    
    keywords = ["불면증", "수면", "잠", "sleep"]
    results = []
    
    for file_path in target_files:
        print(f"Processing: {file_path}")
        df = pd.read_csv(file_path)
        initial_count = len(df)
        
        # title과 description 합치기 (결측치 처리 포함)
        text_series = df['title'].fillna('') + ' ' + df['description'].fillna('')
        
        # 키워드 포함 여부 체크 (대소문자 구분 없이)
        mask = text_series.str.contains('|'.join(keywords), case=False, na=False)
        
        filtered_df = df[mask]
        final_count = len(filtered_df)
        
        filtered_df.to_csv(file_path, index=False, encoding='utf-8-sig')
        
        removed_count = initial_count - final_count
        print(f"  -> Initial: {initial_count}, Filtered: {final_count}, Removed: {removed_count}")
        
        results.append({
            "filename": os.path.basename(file_path),
            "initial_count": initial_count,
            "filtered_count": final_count,
            "removed_count": removed_count
        })
    
    # 결과 요약 저장
    if results:
        results_df = pd.DataFrame(results)
        output_path = "/Users/juns/Desktop/fcicb7/project-1/data/filter_results.csv"
        results_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"\nSummary saved to: {output_path}")

if __name__ == "__main__":
    filter_articles()
