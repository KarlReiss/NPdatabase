#!/usr/bin/env python3
"""
将TTD的UniProt Entry Name转换为UniProt Accession
"""
import pandas as pd
import requests
import time
from pathlib import Path

TTD_FILE = Path(__file__).parent.parent / 'data' / 'TTD' / 'TTD_target_basic_info.csv'
OUTPUT_FILE = Path(__file__).parent.parent / 'data' / 'TTD' / 'TTD_with_accession.csv'

def convert_entry_name_to_accession(entry_names):
    """批量转换UniProt Entry Name到Accession"""
    # 使用简单的搜索API，每次查询一个
    results = {}

    for idx, entry_name in enumerate(entry_names):
        if (idx + 1) % 100 == 0:
            print(f"已处理 {idx + 1}/{len(entry_names)}...")

        try:
            url = f'https://rest.uniprot.org/uniprotkb/search?query=id:{entry_name}&format=tsv&fields=accession,id'
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                if len(lines) > 1:  # 有结果（第一行是表头）
                    parts = lines[1].split('\t')
                    if len(parts) >= 2:
                        accession = parts[0]
                        results[entry_name] = accession

            time.sleep(0.2)  # 避免请求过快

        except Exception as e:
            print(f"转换 {entry_name} 出错: {e}")
            continue

    return results

# 读取TTD数据
print("读取TTD数据...")
ttd_df = pd.read_csv(TTD_FILE)
print(f"TTD记录数: {len(ttd_df)}")

# 获取所有Entry Name
entry_names = ttd_df['UNIPROID'].dropna().unique().tolist()
print(f"需要转换的Entry Name数量: {len(entry_names)}")

# 转换
print("\n开始转换...")
mapping = convert_entry_name_to_accession(entry_names)
print(f"成功转换: {len(mapping)} 个")

# 添加Accession列
ttd_df['UNIPROT_ACCESSION'] = ttd_df['UNIPROID'].map(mapping)

# 保存结果
ttd_df.to_csv(OUTPUT_FILE, index=False)
print(f"\n转换完成！")
print(f"输出文件: {OUTPUT_FILE}")
print(f"有Accession的记录数: {ttd_df['UNIPROT_ACCESSION'].notna().sum()}")
