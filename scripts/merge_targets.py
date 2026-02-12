#!/usr/bin/env python3
"""
合并CMAUP、NPASS和TTD的靶点数据
使用Uniprot ID作为主键去重，用TTD数据补充信息
"""

import pandas as pd
import os

# 文件路径
CMAUP_FILE = '/home/yfguo/NPdatabase/data/CMAUP/CMAUPv2.0_download_Targets.txt'
NPASS_FILE = '/home/yfguo/NPdatabase/data/NPASS/NPASS3.0_target.txt'
TTD_FILE = '/home/yfguo/NPdatabase/data/TTD/TTD_target_basic_info.csv'
OUTPUT_FILE = '/home/yfguo/NPdatabase/data/processed/merged_targets.tsv'

# 确保输出目录存在
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

print("读取CMAUP数据...")
cmaup_df = pd.read_csv(CMAUP_FILE, sep='\t')
print(f"CMAUP: {len(cmaup_df)} 条记录")
print(f"CMAUP列: {list(cmaup_df.columns)}")

print("\n读取NPASS数据...")
npass_df = pd.read_csv(NPASS_FILE, sep='\t')
print(f"NPASS: {len(npass_df)} 条记录")
print(f"NPASS列: {list(npass_df.columns)}")

print("\n读取TTD数据...")
ttd_df = pd.read_csv(TTD_FILE, encoding='utf-8-sig')
print(f"TTD: {len(ttd_df)} 条记录")
print(f"TTD列: {list(ttd_df.columns)}")

# 过滤NPASS数据，只保留蛋白质相关的靶点
protein_types = ['Individual protein', 'Single protein', 'Protein complex',
                 'Protein family', 'Protein-protein interaction',
                 'Protein complex group', 'Chimeric protein']
npass_proteins = npass_df[npass_df['target_type'].isin(protein_types)].copy()
print(f"\nNPASS蛋白质靶点: {len(npass_proteins)} 条记录")

# 标准化列名
cmaup_df = cmaup_df.rename(columns={
    'Target_ID': 'target_id',
    'Gene_Symbol': 'gene_symbol',
    'Protein_Name': 'protein_name',
    'Uniprot_ID': 'uniprot_id',
    'ChEMBL_ID': 'chembl_id',
    'TTD_ID': 'ttd_id'
})

npass_proteins = npass_proteins.rename(columns={
    'target_id': 'npass_id',
    'target_name': 'protein_name',
    'uniprot_id': 'uniprot_id',
    'target_organism': 'organism'
})

ttd_df = ttd_df.rename(columns={
    'TARGETID': 'ttd_id',
    'UNIPROID': 'uniprot_id_ttd',
    'TARGNAME': 'ttd_target_name',
    'GENENAME': 'gene_symbol_ttd',
    'TARGTYPE': 'ttd_target_type',
    'FUNCTION': 'function',
    'BIOCLASS': 'bioclass'
})

# 清理uniprot_id（去除空值和'n.a.'）
def clean_uniprot(df, col):
    df[col] = df[col].replace(['n.a.', 'NA', 'N/A', ''], pd.NA)
    df[col] = df[col].str.strip()
    return df

cmaup_df = clean_uniprot(cmaup_df, 'uniprot_id')
npass_proteins = clean_uniprot(npass_proteins, 'uniprot_id')
ttd_df = clean_uniprot(ttd_df, 'uniprot_id_ttd')

# 只保留有uniprot_id的记录
cmaup_valid = cmaup_df[cmaup_df['uniprot_id'].notna()].copy()
npass_valid = npass_proteins[npass_proteins['uniprot_id'].notna()].copy()
ttd_valid = ttd_df[ttd_df['uniprot_id_ttd'].notna()].copy()

print(f"\nCMAUP有效Uniprot ID: {len(cmaup_valid)}")
print(f"NPASS有效Uniprot ID: {len(npass_valid)}")
print(f"TTD有效Uniprot ID: {len(ttd_valid)}")

# 添加数据源标记
cmaup_valid['source'] = 'CMAUP'
npass_valid['source'] = 'NPASS'

# 合并CMAUP和NPASS
# 选择需要的列
cmaup_selected = cmaup_valid[[
    'target_id', 'gene_symbol', 'protein_name', 'uniprot_id',
    'chembl_id', 'ttd_id', 'source'
]].copy()

npass_selected = npass_valid[[
    'npass_id', 'protein_name', 'uniprot_id', 'organism', 'source'
]].copy()
npass_selected = npass_selected.rename(columns={'npass_id': 'target_id'})
# 为NPASS添加缺失的列
npass_selected['gene_symbol'] = pd.NA
npass_selected['chembl_id'] = pd.NA
npass_selected['ttd_id'] = pd.NA

# 为CMAUP添加organism列
cmaup_selected['organism'] = pd.NA

# 合并两个数据集
merged = pd.concat([cmaup_selected, npass_selected], ignore_index=True)
print(f"\n合并后总记录数: {len(merged)}")

# 按uniprot_id去重，优先保留CMAUP的数据（因为信息更完整）
merged = merged.sort_values('source', ascending=True)  # CMAUP在前
merged_dedup = merged.drop_duplicates(subset=['uniprot_id'], keep='first')
print(f"去重后记录数: {len(merged_dedup)}")

# 用TTD数据补充信息
ttd_supplement = ttd_valid[[
    'ttd_id', 'uniprot_id_ttd', 'ttd_target_name', 'gene_symbol_ttd',
    'ttd_target_type', 'function', 'bioclass'
]]

# 合并TTD数据
final_df = merged_dedup.merge(
    ttd_supplement,
    left_on='uniprot_id',
    right_on='uniprot_id_ttd',
    how='left'
)

# 填充缺失的gene_symbol
final_df['gene_symbol'] = final_df['gene_symbol'].fillna(final_df['gene_symbol_ttd'])
# 填充缺失的ttd_id（从TTD合并过来的）
if 'ttd_id_x' in final_df.columns and 'ttd_id_y' in final_df.columns:
    final_df['ttd_id'] = final_df['ttd_id_x'].fillna(final_df['ttd_id_y'])
    final_df = final_df.drop(columns=['ttd_id_x', 'ttd_id_y'])
elif 'ttd_id_y' in final_df.columns:
    final_df['ttd_id'] = final_df.get('ttd_id', pd.Series([pd.NA]*len(final_df))).fillna(final_df['ttd_id_y'])
    final_df = final_df.drop(columns=['ttd_id_y'])

# 删除重复列
final_df = final_df.drop(columns=['uniprot_id_ttd', 'gene_symbol_ttd'])

# 重新排列列顺序
column_order = [
    'target_id', 'uniprot_id', 'gene_symbol', 'protein_name',
    'ttd_id', 'chembl_id', 'organism', 'ttd_target_type',
    'bioclass', 'function', 'source'
]
final_df = final_df[column_order]

# 保存结果
final_df.to_csv(OUTPUT_FILE, sep='\t', index=False)
print(f"\n合并完成！")
print(f"最终靶点数: {len(final_df)}")
print(f"输出文件: {OUTPUT_FILE}")

# 统计信息
print("\n数据源统计:")
print(final_df['source'].value_counts())
print("\n有TTD信息的靶点数:", final_df['ttd_id'].notna().sum())
print("有ChEMBL ID的靶点数:", final_df['chembl_id'].notna().sum())
print("有生物分类信息的靶点数:", final_df['bioclass'].notna().sum())
