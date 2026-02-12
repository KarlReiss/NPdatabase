#!/usr/bin/env python3
"""
合并NPASS、CMAUP和TTD数据库
"""
import pandas as pd
from pathlib import Path

# 文件路径
DATA_DIR = Path(__file__).parent.parent / 'data'
NPASS_COMPOUNDS_FILE = DATA_DIR / 'NPASS' / 'NPASS3.0_naturalproducts_generalinfo.txt'
NPASS_STRUCTURE_FILE = DATA_DIR / 'NPASS' / 'NPASS3.0_naturalproducts_structure.txt'
NPASS_TARGET_FILE = DATA_DIR / 'NPASS' / 'NPASS3.0_target.txt'
CMAUP_INGREDIENTS_FILE = DATA_DIR / 'CMAUP' / 'CMAUPv2.0_download_Ingredients_All.txt'
CMAUP_TARGETS_FILE = DATA_DIR / 'CMAUP' / 'CMAUPv2.0_download_Ingredient_Target_Associations_ActivityValues_References.txt'
TTD_FILE = DATA_DIR / 'TTD' / 'TTD_with_accession.csv'
OUTPUT_DIR = DATA_DIR / 'processed'
OUTPUT_FILE = OUTPUT_DIR / 'merged_compounds.csv'
TARGETS_FILE = OUTPUT_DIR / 'merged_targets.csv'

def load_npass():
    """加载NPASS化合物数据"""
    print("\n加载NPASS数据...")

    # 加载化合物基本信息
    print("读取化合物基本信息...")
    compounds_df = pd.read_csv(NPASS_COMPOUNDS_FILE, sep='\t', low_memory=False)

    # 加载结构信息
    print("读取结构信息...")
    structure_df = pd.read_csv(NPASS_STRUCTURE_FILE, sep='\t', low_memory=False)

    # 合并数据
    df = pd.merge(compounds_df, structure_df, on='np_id', how='left')

    records = []
    for _, row in df.iterrows():
        records.append({
            'source': 'NPASS',
            'compound_id': row.get('np_id'),
            'compound_name': row.get('name'),
            'smiles': row.get('smiles'),
            'inchi': row.get('inchi'),
            'inchikey': row.get('inchikey'),
            'molecular_formula': row.get('molecular_formula'),
            'molecular_weight': row.get('molecular_weight'),
        })

    result_df = pd.DataFrame(records)
    print(f"NPASS记录数: {len(result_df)}")
    return result_df

def load_cmaup():
    """加载CMAUP化合物数据"""
    print("\n加载CMAUP数据...")
    df = pd.read_csv(CMAUP_INGREDIENTS_FILE, sep='\t', low_memory=False)

    records = []
    for _, row in df.iterrows():
        records.append({
            'source': 'CMAUP',
            'compound_id': row.get('Ingredient_id'),
            'compound_name': row.get('Ingredient_name'),
            'smiles': row.get('SMILES'),
            'inchi': row.get('InChI'),
            'inchikey': row.get('InChIKey'),
            'molecular_formula': row.get('Molecular_Formula'),
            'molecular_weight': row.get('Molecular_Weight'),
        })

    result_df = pd.DataFrame(records)
    print(f"CMAUP记录数: {len(result_df)}")
    return result_df

def load_npass_targets():
    """加载NPASS靶点数据"""
    print("\n加载NPASS靶点数据...")
    df = pd.read_csv(NPASS_TARGET_FILE, sep='\t', low_memory=False)

    records = []
    for _, row in df.iterrows():
        records.append({
            'source': 'NPASS',
            'compound_id': row.get('np_id'),
            'target_name': row.get('target_name'),
            'uniprot_id': row.get('uniprot_id'),
            'activity_type': row.get('activity_type'),
            'activity_value': row.get('activity_value'),
        })

    result_df = pd.DataFrame(records)
    print(f"NPASS靶点记录数: {len(result_df)}")
    return result_df

def load_cmaup_targets():
    """加载CMAUP靶点数据"""
    print("\n加载CMAUP靶点数据...")
    df = pd.read_csv(CMAUP_TARGETS_FILE, sep='\t', low_memory=False)

    records = []
    for _, row in df.iterrows():
        records.append({
            'source': 'CMAUP',
            'compound_id': row.get('Ingredient_id'),
            'target_name': row.get('Target_name'),
            'uniprot_id': row.get('UniProt_id'),
            'activity_type': row.get('Activity_type'),
            'activity_value': row.get('Activity_value'),
        })

    result_df = pd.DataFrame(records)
    print(f"CMAUP靶点记录数: {len(result_df)}")
    return result_df

def load_ttd():
    """加载TTD靶点数据"""
    print("\n加载TTD数据...")
    df = pd.read_csv(TTD_FILE, low_memory=False)

    records = []
    for _, row in df.iterrows():
        records.append({
            'source': 'TTD',
            'target_id': row.get('TARGETID'),
            'target_name': row.get('TARGNAME'),
            'target_type': row.get('TARGTYPE'),
            'uniprot_id': row.get('UNIPROID'),
            'gene_name': row.get('GENENAME'),
        })

    result_df = pd.DataFrame(records)
    print(f"TTD记录数: {len(result_df)}")
    print(f"有UniProt ID的记录: {result_df['uniprot_id'].notna().sum()}")
    return result_df

def main():
    print("=" * 60)
    print("开始合并数据库")
    print("=" * 60)

    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 加载化合物数据
    npass_df = load_npass()
    cmaup_df = load_cmaup()

    # 加载靶点数据
    npass_targets_df = load_npass_targets()
    cmaup_targets_df = load_cmaup_targets()
    ttd_df = load_ttd()

    # 合并化合物数据
    compounds_df = pd.concat([npass_df, cmaup_df], ignore_index=True)

    # 合并靶点数据
    targets_df = pd.concat([npass_targets_df, cmaup_targets_df, ttd_df], ignore_index=True)

    print("\n" + "=" * 60)
    print("合并统计:")
    print(f"化合物总数: {len(compounds_df)}")
    print(f"  - NPASS: {len(npass_df)}")
    print(f"  - CMAUP: {len(cmaup_df)}")
    print(f"靶点总数: {len(targets_df)}")
    print(f"  - NPASS: {len(npass_targets_df)}")
    print(f"  - CMAUP: {len(cmaup_targets_df)}")
    print(f"  - TTD: {len(ttd_df)}")
    print("=" * 60)

    # 保存合并结果
    print(f"\n保存化合物数据到: {OUTPUT_FILE}")
    compounds_df.to_csv(OUTPUT_FILE, index=False)

    print(f"保存靶点数据到: {TARGETS_FILE}")
    targets_df.to_csv(TARGETS_FILE, index=False)

    print("\n合并完成！")

if __name__ == '__main__':
    main()
