#!/usr/bin/env python3
"""
合并 CMAUP 和 NPASS 靶点数据
策略：以 NPASS 为基础（包含更多靶点），用 CMAUP 的详细注释信息进行补充
"""

import pandas as pd
import os

# 读取数据
print("读取数据文件...")
cmaup = pd.read_csv('/home/yfguo/NPdatabase/data/CMAUP/CMAUPv2.0_download_Targets.txt', sep='\t')
npass = pd.read_csv('/home/yfguo/NPdatabase/data/NPASS/NPASS3.0_target.txt', sep='\t')

print(f"CMAUP 靶点数: {len(cmaup)}")
print(f"NPASS 靶点数: {len(npass)}")

# 重命名 NPASS 列以保持一致性
npass_renamed = npass.rename(columns={
    'target_id': 'Target_ID',
    'target_type': 'NPASS_Target_Type',
    'target_name': 'Target_Name',
    'target_organism_tax_id': 'Organism_Tax_ID',
    'target_organism': 'Organism',
    'uniprot_id': 'Uniprot_ID'
})

# 重命名 CMAUP 列以避免冲突
cmaup_renamed = cmaup.rename(columns={
    'Protein_Name': 'CMAUP_Protein_Name',
    'Target_type': 'CMAUP_Target_Type'
})

# 合并数据：左连接，保留所有 NPASS 数据
print("\n合并数据...")
merged = npass_renamed.merge(
    cmaup_renamed,
    on='Target_ID',
    how='left',
    suffixes=('', '_cmaup')
)

# 处理 Uniprot_ID：优先使用 CMAUP 的（更可靠），如果没有则使用 NPASS 的
merged['Uniprot_ID_Final'] = merged['Uniprot_ID_cmaup'].fillna(merged['Uniprot_ID'])

# 处理 Target_Name：优先使用 CMAUP 的蛋白名称，否则使用 NPASS 的
merged['Target_Name_Final'] = merged['CMAUP_Protein_Name'].fillna(merged['Target_Name'])

# 选择最终的列并重新排序
final_columns = [
    'Target_ID',
    'Gene_Symbol',
    'Target_Name_Final',
    'Uniprot_ID_Final',
    'NPASS_Target_Type',
    'CMAUP_Target_Type',
    'Organism_Tax_ID',
    'Organism',
    'ChEMBL_ID',
    'TTD_ID',
    'if_DTP',
    'if_CYP',
    'if_therapeutic_target',
    'Target_Class_Level1',
    'Target_Class_Level2',
    'Target_Class_Level3',
    'Target_Class_level_displayed'
]

result = merged[final_columns].rename(columns={
    'Target_Name_Final': 'Target_Name',
    'Uniprot_ID_Final': 'Uniprot_ID'
})

# 统计信息
print("\n=== 合并结果统计 ===")
print(f"总靶点数: {len(result)}")
print(f"有 CMAUP 注释的靶点: {result['Gene_Symbol'].notna().sum()}")
print(f"仅 NPASS 数据的靶点: {result['Gene_Symbol'].isna().sum()}")
print(f"有效 Uniprot_ID (非 n.a.): {(result['Uniprot_ID'] != 'n.a.').sum()}")
print(f"有 ChEMBL_ID: {result['ChEMBL_ID'].notna().sum()}")
print(f"有 TTD_ID: {result['TTD_ID'].notna().sum()}")
print(f"治疗靶点: {(result['if_therapeutic_target'] == 1).sum()}")

# 创建输出目录
output_dir = '/home/yfguo/NPdatabase/data/processed'
os.makedirs(output_dir, exist_ok=True)

# 保存结果
output_file = os.path.join(output_dir, 'merged_targets.tsv')
result.to_csv(output_file, sep='\t', index=False)
print(f"\n合并结果已保存到: {output_file}")

# 额外保存一个仅包含蛋白质靶点的版本（排除细胞系、组织等）
protein_types = ['Individual protein', 'Single protein', 'Protein complex', 'Protein family']
protein_targets = result[result['NPASS_Target_Type'].isin(protein_types)]
protein_output = os.path.join(output_dir, 'merged_targets_proteins_only.tsv')
protein_targets.to_csv(protein_output, sep='\t', index=False)
print(f"蛋白质靶点已保存到: {protein_output}")
print(f"蛋白质靶点数: {len(protein_targets)}")

print("\n完成！")
