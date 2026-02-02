#!/usr/bin/env python3
"""
导入天然产物数据到 natural_products 表
数据源: NPASS + CMAUP
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from datetime import datetime

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'npdb',
    'user': 'yfguo',
    'host': 'localhost',
    'port': 5432
}

# 数据文件路径
DATA_DIR = '/home/yfguo/NPdatabase/data'
NPASS_GENERAL = f'{DATA_DIR}/NPASS/NPASS3.0_naturalproducts_generalinfo.txt'
NPASS_STRUCTURE = f'{DATA_DIR}/NPASS/NPASS3.0_naturalproducts_structure.txt'
CMAUP_INGREDIENTS = f'{DATA_DIR}/CMAUP/CMAUPv2.0_download_Ingredients_All.txt'


def clean_value(val):
    """清理数据值，将 n.a. 和空字符串转为 None"""
    if pd.isna(val):
        return None
    if isinstance(val, str):
        val = val.strip()
        if val.lower() in ('n.a.', 'n.a', 'na', '', '-'):
            return None
    return val


def load_npass_data():
    """加载NPASS数据"""
    print(f"[{datetime.now()}] 加载 NPASS generalinfo...")
    df_general = pd.read_csv(NPASS_GENERAL, sep='\t', dtype=str)
    print(f"  - 记录数: {len(df_general)}")

    print(f"[{datetime.now()}] 加载 NPASS structure...")
    df_structure = pd.read_csv(NPASS_STRUCTURE, sep='\t', dtype=str)
    print(f"  - 记录数: {len(df_structure)}")

    # 合并 generalinfo 和 structure
    print(f"[{datetime.now()}] 合并 NPASS 数据...")
    df_npass = df_general.merge(df_structure, on='np_id', how='left')
    print(f"  - 合并后记录数: {len(df_npass)}")

    return df_npass


def load_cmaup_data():
    """加载CMAUP数据"""
    print(f"[{datetime.now()}] 加载 CMAUP Ingredients...")
    df_cmaup = pd.read_csv(CMAUP_INGREDIENTS, sep='\t', dtype=str)
    print(f"  - 记录数: {len(df_cmaup)}")

    # 重命名列以匹配
    df_cmaup = df_cmaup.rename(columns={
        'pubchem_cid': 'pubchem_id',
        'MW': 'molecular_weight',
        'LogP': 'xlogp',
        'TPSA': 'psa',
        'nHD': 'h_bond_donors',
        'nHA': 'h_bond_acceptors',
        'nRot': 'rotatable_bonds'
    })

    return df_cmaup


def merge_data(df_npass, df_cmaup):
    """合并NPASS和CMAUP数据"""
    print(f"[{datetime.now()}] 合并 NPASS 和 CMAUP 数据...")

    # CMAUP中需要补充的字段
    cmaup_cols = ['np_id', 'molecular_weight', 'xlogp', 'psa',
                  'h_bond_donors', 'h_bond_acceptors', 'rotatable_bonds']
    df_cmaup_subset = df_cmaup[cmaup_cols].copy()

    # 左连接，以NPASS为主
    df_merged = df_npass.merge(df_cmaup_subset, on='np_id', how='left', suffixes=('', '_cmaup'))

    # 用CMAUP数据补充空值
    for col in ['molecular_weight', 'xlogp', 'psa', 'h_bond_donors', 'h_bond_acceptors', 'rotatable_bonds']:
        if col in df_merged.columns and f'{col}_cmaup' in df_merged.columns:
            df_merged[col] = df_merged[col].fillna(df_merged[f'{col}_cmaup'])
            df_merged = df_merged.drop(columns=[f'{col}_cmaup'])

    # 添加CMAUP中独有的记录（不在NPASS中的）
    npass_np_ids = set(df_npass['np_id'].unique())
    df_cmaup_only = df_cmaup[~df_cmaup['np_id'].isin(npass_np_ids)].copy()

    if len(df_cmaup_only) > 0:
        print(f"  - CMAUP独有记录: {len(df_cmaup_only)}")
        # 确保列对齐
        for col in df_merged.columns:
            if col not in df_cmaup_only.columns:
                df_cmaup_only[col] = None
        df_cmaup_only = df_cmaup_only[df_merged.columns]
        df_merged = pd.concat([df_merged, df_cmaup_only], ignore_index=True)

    print(f"  - 最终记录数: {len(df_merged)}")
    return df_merged


def prepare_records(df):
    """准备插入数据库的记录"""
    print(f"[{datetime.now()}] 准备数据库记录...")

    records = []
    for _, row in df.iterrows():
        record = {
            'np_id': clean_value(row.get('np_id')),
            'inchikey': clean_value(row.get('InChIKey') or row.get('inchikey')),
            'pref_name': clean_value(row.get('pref_name')),
            'iupac_name': clean_value(row.get('iupac_name')),
            'name_initial': clean_value(row.get('name_initial')),
            'inchi': clean_value(row.get('InChI') or row.get('inchi')),
            'smiles': clean_value(row.get('SMILES') or row.get('smiles')),
            'chembl_id': clean_value(row.get('chembl_id')),
            'pubchem_id': clean_value(row.get('pubchem_id')),
            'molecular_weight': None,
            'xlogp': None,
            'psa': None,
            'h_bond_donors': None,
            'h_bond_acceptors': None,
            'rotatable_bonds': None,
            'num_of_organism': None,
            'num_of_target': None,
            'num_of_activity': None,
            'gene_cluster': clean_value(row.get('gene_cluster')),
            'if_quantity': str(row.get('ifQuantity', '')).lower() == 'yes' if pd.notna(row.get('ifQuantity')) else False
        }

        # 数值字段转换
        try:
            mw = clean_value(row.get('molecular_weight'))
            record['molecular_weight'] = float(mw) if mw else None
        except (ValueError, TypeError):
            pass

        try:
            xlogp = clean_value(row.get('xlogp'))
            record['xlogp'] = float(xlogp) if xlogp else None
        except (ValueError, TypeError):
            pass

        try:
            psa = clean_value(row.get('psa'))
            record['psa'] = float(psa) if psa else None
        except (ValueError, TypeError):
            pass

        try:
            hbd = clean_value(row.get('h_bond_donors'))
            record['h_bond_donors'] = int(float(hbd)) if hbd else None
        except (ValueError, TypeError):
            pass

        try:
            hba = clean_value(row.get('h_bond_acceptors'))
            record['h_bond_acceptors'] = int(float(hba)) if hba else None
        except (ValueError, TypeError):
            pass

        try:
            rot = clean_value(row.get('rotatable_bonds'))
            record['rotatable_bonds'] = int(float(rot)) if rot else None
        except (ValueError, TypeError):
            pass

        try:
            num_org = clean_value(row.get('num_of_organism'))
            record['num_of_organism'] = int(num_org) if num_org else 0
        except (ValueError, TypeError):
            record['num_of_organism'] = 0

        try:
            num_tgt = clean_value(row.get('num_of_target'))
            record['num_of_target'] = int(num_tgt) if num_tgt else 0
        except (ValueError, TypeError):
            record['num_of_target'] = 0

        try:
            num_act = clean_value(row.get('num_of_activity'))
            record['num_of_activity'] = int(num_act) if num_act else 0
        except (ValueError, TypeError):
            record['num_of_activity'] = 0

        # 跳过没有np_id的记录
        if record['np_id']:
            records.append(record)

    print(f"  - 有效记录数: {len(records)}")
    return records


def insert_to_db(records, batch_size=5000):
    """批量插入数据库"""
    # 先按np_id去重，保留第一条
    print(f"[{datetime.now()}] 去重处理...")
    seen = set()
    unique_records = []
    for r in records:
        if r['np_id'] not in seen:
            seen.add(r['np_id'])
            unique_records.append(r)
    records = unique_records
    print(f"  - 去重后记录数: {len(records)}")

    print(f"[{datetime.now()}] 连接数据库...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # 插入SQL
    insert_sql = """
        INSERT INTO natural_products (
            np_id, inchikey, pref_name, iupac_name, name_initial,
            inchi, smiles, chembl_id, pubchem_id,
            molecular_weight, xlogp, psa,
            h_bond_donors, h_bond_acceptors, rotatable_bonds,
            num_of_organism, num_of_target, num_of_activity,
            gene_cluster, if_quantity
        ) VALUES %s
        ON CONFLICT (np_id) DO UPDATE SET
            inchikey = COALESCE(EXCLUDED.inchikey, natural_products.inchikey),
            pref_name = COALESCE(EXCLUDED.pref_name, natural_products.pref_name),
            iupac_name = COALESCE(EXCLUDED.iupac_name, natural_products.iupac_name),
            inchi = COALESCE(EXCLUDED.inchi, natural_products.inchi),
            smiles = COALESCE(EXCLUDED.smiles, natural_products.smiles),
            chembl_id = COALESCE(EXCLUDED.chembl_id, natural_products.chembl_id),
            pubchem_id = COALESCE(EXCLUDED.pubchem_id, natural_products.pubchem_id),
            molecular_weight = COALESCE(EXCLUDED.molecular_weight, natural_products.molecular_weight),
            xlogp = COALESCE(EXCLUDED.xlogp, natural_products.xlogp),
            psa = COALESCE(EXCLUDED.psa, natural_products.psa),
            h_bond_donors = COALESCE(EXCLUDED.h_bond_donors, natural_products.h_bond_donors),
            h_bond_acceptors = COALESCE(EXCLUDED.h_bond_acceptors, natural_products.h_bond_acceptors),
            rotatable_bonds = COALESCE(EXCLUDED.rotatable_bonds, natural_products.rotatable_bonds),
            updated_at = CURRENT_TIMESTAMP
    """

    # 转换为元组列表
    values = [
        (
            r['np_id'], r['inchikey'], r['pref_name'], r['iupac_name'], r['name_initial'],
            r['inchi'], r['smiles'], r['chembl_id'], r['pubchem_id'],
            r['molecular_weight'], r['xlogp'], r['psa'],
            r['h_bond_donors'], r['h_bond_acceptors'], r['rotatable_bonds'],
            r['num_of_organism'], r['num_of_target'], r['num_of_activity'],
            r['gene_cluster'], r['if_quantity']
        )
        for r in records
    ]

    # 批量插入
    total = len(values)
    inserted = 0

    print(f"[{datetime.now()}] 开始插入数据 (共 {total} 条)...")

    for i in range(0, total, batch_size):
        batch = values[i:i+batch_size]
        execute_values(cur, insert_sql, batch, page_size=batch_size)
        conn.commit()
        inserted += len(batch)
        print(f"  - 进度: {inserted}/{total} ({100*inserted/total:.1f}%)")

    # 验证
    cur.execute("SELECT COUNT(*) FROM natural_products")
    count = cur.fetchone()[0]
    print(f"[{datetime.now()}] 导入完成! 表中总记录数: {count}")

    cur.close()
    conn.close()

    return count


def main():
    print("=" * 60)
    print("天然产物数据导入脚本")
    print("=" * 60)

    # 加载数据
    df_npass = load_npass_data()
    df_cmaup = load_cmaup_data()

    # 合并数据
    df_merged = merge_data(df_npass, df_cmaup)

    # 准备记录
    records = prepare_records(df_merged)

    # 插入数据库
    count = insert_to_db(records)

    print("=" * 60)
    print(f"导入完成! 共导入 {count} 条天然产物记录")
    print("=" * 60)


if __name__ == '__main__':
    main()
