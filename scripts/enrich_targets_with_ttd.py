#!/usr/bin/env python3
"""
用 TTD 数据补充 merged_targets.tsv
通过 TTD_ID 字段进行匹配
"""

import pandas as pd
import os

# 读取数据
print("读取数据文件...")
merged = pd.read_csv('/home/yfguo/NPdatabase/data/processed/merged_targets.tsv', sep='\t')
ttd = pd.read_csv('/home/yfguo/NPdatabase/data/TTD/TTD_target_basic_info.csv')

print(f"Merged targets: {len(merged)}")
print(f"TTD targets: {len(ttd)}")
print(f"Merged 中有 TTD_ID 的记录: {merged['TTD_ID'].notna().sum()}")

# 选择要从 TTD 补充的字段
ttd_fields = {
    'TARGETID': 'TTD_ID',  # 用于匹配
    'FORMERID': 'TTD_Former_ID',
    'UNIPROID': 'TTD_Uniprot_Name',  # TTD的Uniprot Entry Name
    'TARGNAME': 'TTD_Target_Name',
    'GENENAME': 'TTD_Gene_Name',
    'TARGTYPE': 'TTD_Target_Type',
    'SYNONYMS': 'TTD_Synonyms',
    'FUNCTION': 'TTD_Function',
    'PDBSTRUC': 'TTD_PDB_Structures',
    'BIOCLASS': 'TTD_Bio_Class',
    'ECNUMBER': 'TTD_EC_Number',
    'SEQUENCE': 'TTD_Sequence'
}

# 重命名 TTD 列
ttd_renamed = ttd.rename(columns=ttd_fields)

# 合并数据：通过 TTD_ID 左连接
print("\n合并 TTD 数据...")
# 保留 TTD_ID 列用于匹配
ttd_cols_to_merge = [col for col in ttd_fields.values()]
enriched = merged.merge(
    ttd_renamed[ttd_cols_to_merge],
    left_on='TTD_ID',
    right_on='TTD_ID',
    how='left',
    suffixes=('', '_ttd')
)

# 统计补充情况
print("\n=== TTD 数据补充统计 ===")
for new_col in ttd_fields.values():
    if new_col != 'TTD_ID' and new_col in enriched.columns:
        count = enriched[new_col].notna().sum()
        print(f"{new_col}: {count} 条记录")

# 检查是否有 Gene_Symbol 为空但 TTD_Gene_Name 有值的情况
can_fill_gene = (enriched['Gene_Symbol'].isna()) & (enriched['TTD_Gene_Name'].notna())
print(f"\n可以用 TTD_Gene_Name 补充 Gene_Symbol 的记录: {can_fill_gene.sum()}")

# 补充 Gene_Symbol
if can_fill_gene.sum() > 0:
    enriched.loc[can_fill_gene, 'Gene_Symbol'] = enriched.loc[can_fill_gene, 'TTD_Gene_Name']
    print("已补充 Gene_Symbol")

# 保存结果
output_file = '/home/yfguo/NPdatabase/data/processed/merged_targets_enriched.tsv'
enriched.to_csv(output_file, sep='\t', index=False)
print(f"\n补充后的数据已保存到: {output_file}")

# 也更新蛋白质靶点表
print("\n更新蛋白质靶点表...")
protein_types = ['Individual protein', 'Single protein', 'Protein complex', 'Protein family']
protein_targets = enriched[enriched['NPASS_Target_Type'].isin(protein_types)]
protein_output = '/home/yfguo/NPdatabase/data/processed/merged_targets_proteins_only_enriched.tsv'
protein_targets.to_csv(protein_output, sep='\t', index=False)
print(f"蛋白质靶点已保存到: {protein_output}")
print(f"蛋白质靶点数: {len(protein_targets)}")

# 显示样例
print("\n=== 补充后的样例（有TTD数据的记录）===")
sample = enriched[enriched['TTD_ID'].notna()].head(2)
for idx, row in sample.iterrows():
    print(f"\nTarget_ID: {row['Target_ID']}")
    print(f"  Gene_Symbol: {row['Gene_Symbol']}")
    print(f"  TTD_ID: {row['TTD_ID']}")
    print(f"  TTD_Target_Name: {row['TTD_Target_Name']}")
    print(f"  TTD_Bio_Class: {row['TTD_Bio_Class']}")
    print(f"  TTD_PDB_Structures: {row['TTD_PDB_Structures'][:50] if pd.notna(row['TTD_PDB_Structures']) else 'N/A'}...")
    print(f"  TTD_EC_Number: {row['TTD_EC_Number']}")

print("\n完成！")
