#!/usr/bin/env python3
"""
导入生物资源数据到 bio_resources 表
数据源: NPASS species_info + CMAUP Plants
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
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
NPASS_SPECIES = f'{DATA_DIR}/NPASS/NPASS3.0_species_info.txt'
CMAUP_PLANTS = f'{DATA_DIR}/CMAUP/CMAUPv2.0_download_Plants.txt'


def clean_value(val):
    """清理数据值，将 n.a. 和空字符串转为 None"""
    if pd.isna(val):
        return None
    if isinstance(val, str):
        val = val.strip()
        if val.lower() in ('n.a.', 'n.a', 'na', '', '-'):
            return None
    return val


def infer_resource_type(kingdom_name, superkingdom_name):
    """根据分类学信息推断资源类型"""
    kingdom = str(kingdom_name).lower() if kingdom_name else ''
    superkingdom = str(superkingdom_name).lower() if superkingdom_name else ''

    if 'viridiplantae' in kingdom or 'plant' in kingdom:
        return 'Plant'
    elif 'fungi' in kingdom:
        return 'Microbe'
    elif 'bacteria' in superkingdom or 'archaea' in superkingdom:
        return 'Microbe'
    elif 'metazoa' in kingdom or 'animal' in kingdom:
        return 'Animal'
    elif superkingdom == 'eukaryota':
        # 真核生物但不是植物、动物、真菌，可能是原生生物等
        return 'Microbe'
    else:
        return 'Other'


def load_npass_species():
    """加载NPASS物种数据"""
    print(f"[{datetime.now()}] 加载 NPASS species_info...")
    df = pd.read_csv(NPASS_SPECIES, sep='\t', dtype=str)
    print(f"  - 记录数: {len(df)}")
    print(f"  - 列名: {list(df.columns)}")
    return df


def load_cmaup_plants():
    """加载CMAUP植物数据"""
    print(f"[{datetime.now()}] 加载 CMAUP Plants...")
    df = pd.read_csv(CMAUP_PLANTS, sep='\t', dtype=str)
    print(f"  - 记录数: {len(df)}")
    print(f"  - 列名: {list(df.columns)}")
    return df


def prepare_records(df_npass, df_cmaup):
    """准备插入数据库的记录"""
    print(f"[{datetime.now()}] 准备数据库记录...")

    records = []
    seen_ids = set()

    # 处理NPASS数据
    for _, row in df_npass.iterrows():
        resource_id = clean_value(row.get('org_id'))
        if not resource_id or resource_id in seen_ids:
            continue
        seen_ids.add(resource_id)

        kingdom_name = clean_value(row.get('kingdom_name'))
        superkingdom_name = clean_value(row.get('superkingdom_name'))
        resource_type = infer_resource_type(kingdom_name, superkingdom_name)

        record = {
            'resource_id': resource_id,
            'resource_type': resource_type,
            'latin_name': clean_value(row.get('org_name')),
            'taxonomy_kingdom': kingdom_name,
            'taxonomy_family': clean_value(row.get('family_name')),
            'taxonomy_genus': clean_value(row.get('genus_name')),
            'taxonomy_species': clean_value(row.get('species_name')),
            'taxonomy_id': clean_value(row.get('species_tax_id')),
            # NPASS额外字段
            'num_of_natural_products': 0,
        }

        # 统计天然产物数量
        try:
            num_act = int(row.get('num_of_np_act', 0) or 0)
            num_no_act = int(row.get('num_of_np_no_act', 0) or 0)
            record['num_of_natural_products'] = num_act + num_no_act
        except (ValueError, TypeError):
            pass

        records.append(record)

    print(f"  - NPASS物种数: {len(records)}")

    # 处理CMAUP数据（补充不在NPASS中的）
    cmaup_added = 0
    for _, row in df_cmaup.iterrows():
        resource_id = clean_value(row.get('Plant_ID'))
        if not resource_id or resource_id in seen_ids:
            continue
        seen_ids.add(resource_id)

        record = {
            'resource_id': resource_id,
            'resource_type': 'Plant',  # CMAUP都是植物
            'latin_name': clean_value(row.get('Plant_Name')),
            'taxonomy_kingdom': 'Viridiplantae',
            'taxonomy_family': clean_value(row.get('Family_Name')),
            'taxonomy_genus': clean_value(row.get('Genus_Name')),
            'taxonomy_species': clean_value(row.get('Species_Name')),
            'taxonomy_id': clean_value(row.get('Species_Tax_ID')),
            'num_of_natural_products': 0,
        }
        records.append(record)
        cmaup_added += 1

    print(f"  - CMAUP新增植物数: {cmaup_added}")
    print(f"  - 总生物资源数: {len(records)}")

    # 统计资源类型分布
    type_counts = {}
    for r in records:
        t = r['resource_type']
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"  - 资源类型分布: {type_counts}")

    return records


def insert_to_db(records, batch_size=2000):
    """批量插入数据库"""
    print(f"[{datetime.now()}] 连接数据库...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # 插入SQL
    insert_sql = """
        INSERT INTO bio_resources (
            resource_id, resource_type, latin_name,
            taxonomy_kingdom, taxonomy_family, taxonomy_genus,
            taxonomy_species, taxonomy_id, num_of_natural_products
        ) VALUES %s
        ON CONFLICT (resource_id) DO UPDATE SET
            resource_type = COALESCE(EXCLUDED.resource_type, bio_resources.resource_type),
            latin_name = COALESCE(EXCLUDED.latin_name, bio_resources.latin_name),
            taxonomy_kingdom = COALESCE(EXCLUDED.taxonomy_kingdom, bio_resources.taxonomy_kingdom),
            taxonomy_family = COALESCE(EXCLUDED.taxonomy_family, bio_resources.taxonomy_family),
            taxonomy_genus = COALESCE(EXCLUDED.taxonomy_genus, bio_resources.taxonomy_genus),
            taxonomy_species = COALESCE(EXCLUDED.taxonomy_species, bio_resources.taxonomy_species),
            taxonomy_id = COALESCE(EXCLUDED.taxonomy_id, bio_resources.taxonomy_id),
            updated_at = CURRENT_TIMESTAMP
    """

    # 转换为元组列表
    values = [
        (
            r['resource_id'], r['resource_type'], r['latin_name'],
            r['taxonomy_kingdom'], r['taxonomy_family'], r['taxonomy_genus'],
            r['taxonomy_species'], r['taxonomy_id'], r['num_of_natural_products']
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
    cur.execute("SELECT COUNT(*) FROM bio_resources")
    count = cur.fetchone()[0]
    print(f"[{datetime.now()}] 导入完成! 表中总记录数: {count}")

    cur.close()
    conn.close()

    return count


def main():
    print("=" * 60)
    print("生物资源数据导入脚本")
    print("=" * 60)

    # 加载数据
    df_npass = load_npass_species()
    df_cmaup = load_cmaup_plants()

    # 准备记录
    records = prepare_records(df_npass, df_cmaup)

    # 插入数据库
    count = insert_to_db(records)

    print("=" * 60)
    print(f"导入完成! 共导入 {count} 条生物资源记录")
    print("=" * 60)


if __name__ == '__main__':
    main()
