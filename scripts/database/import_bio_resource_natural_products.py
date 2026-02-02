#!/usr/bin/env python3
"""
导入生物资源-天然产物关联数据到 bio_resource_natural_products 表
数据源: NPASS naturalproducts_species_pair + CMAUP Plant_Ingredient_Associations
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
NPASS_SPECIES_PAIR = f'{DATA_DIR}/NPASS/NPASS3.0_naturalproducts_species_pair.txt'
CMAUP_PLANT_INGREDIENT = f'{DATA_DIR}/CMAUP/CMAUPv2.0_download_Plant_Ingredient_Associations_allIngredients.txt'


def clean_value(val):
    """清理数据值，将 n.a. 和空字符串转为 None"""
    if pd.isna(val):
        return None
    if isinstance(val, str):
        val = val.strip()
        if val.lower() in ('n.a.', 'n.a', 'na', '', '-'):
            return None
    return val


def load_id_mappings(conn):
    """加载ID映射表"""
    print(f"[{datetime.now()}] 加载ID映射...")
    cur = conn.cursor()

    # natural_products: np_id -> id
    cur.execute("SELECT np_id, id FROM natural_products")
    np_map = {row[0]: row[1] for row in cur.fetchall()}
    print(f"  - natural_products映射: {len(np_map)} 条")

    # bio_resources: resource_id -> id
    cur.execute("SELECT resource_id, id FROM bio_resources")
    br_map = {row[0]: row[1] for row in cur.fetchall()}
    print(f"  - bio_resources映射: {len(br_map)} 条")

    cur.close()
    return np_map, br_map


def process_npass_data(np_map, br_map):
    """处理NPASS关联数据"""
    print(f"[{datetime.now()}] 加载 NPASS species_pair...")

    records = []
    seen_pairs = set()
    skipped_np = 0
    skipped_br = 0
    skipped_dup = 0

    # 分块读取大文件
    chunk_size = 100000
    for chunk_num, chunk in enumerate(pd.read_csv(NPASS_SPECIES_PAIR, sep='\t', dtype=str, chunksize=chunk_size)):
        for _, row in chunk.iterrows():
            np_id = clean_value(row.get('np_id'))
            org_id = clean_value(row.get('org_id'))

            # 查找外键ID
            if np_id not in np_map:
                skipped_np += 1
                continue
            if org_id not in br_map:
                skipped_br += 1
                continue

            # 去重（同一对只保留一条）
            pair_key = (br_map[org_id], np_map[np_id])
            if pair_key in seen_pairs:
                skipped_dup += 1
                continue
            seen_pairs.add(pair_key)

            record = {
                'bio_resource_id': br_map[org_id],
                'natural_product_id': np_map[np_id],
                'content_part': clean_value(row.get('org_isolation_part')),
                'ref_id': clean_value(row.get('ref_id')),
                'ref_id_type': clean_value(row.get('ref_id_type')),
            }
            records.append(record)

        print(f"  - 已处理 {(chunk_num + 1) * chunk_size} 行...")

    print(f"  - NPASS有效记录: {len(records)}")
    print(f"  - 跳过(无匹配NP): {skipped_np}")
    print(f"  - 跳过(无匹配BR): {skipped_br}")
    print(f"  - 跳过(重复): {skipped_dup}")

    return records, seen_pairs


def process_cmaup_data(np_map, br_map, seen_pairs):
    """处理CMAUP关联数据"""
    print(f"[{datetime.now()}] 加载 CMAUP Plant_Ingredient...")

    # CMAUP文件没有表头
    df = pd.read_csv(CMAUP_PLANT_INGREDIENT, sep='\t', dtype=str, header=None,
                     names=['Plant_ID', 'Ingredient_ID'])
    print(f"  - 原始记录数: {len(df)}")

    records = []
    skipped_np = 0
    skipped_br = 0
    skipped_dup = 0

    for _, row in df.iterrows():
        np_id = clean_value(row.get('Ingredient_ID'))
        org_id = clean_value(row.get('Plant_ID'))

        # 查找外键ID
        if np_id not in np_map:
            skipped_np += 1
            continue
        if org_id not in br_map:
            skipped_br += 1
            continue

        # 去重
        pair_key = (br_map[org_id], np_map[np_id])
        if pair_key in seen_pairs:
            skipped_dup += 1
            continue
        seen_pairs.add(pair_key)

        record = {
            'bio_resource_id': br_map[org_id],
            'natural_product_id': np_map[np_id],
            'content_part': None,
            'ref_id': None,
            'ref_id_type': None,
        }
        records.append(record)

    print(f"  - CMAUP新增记录: {len(records)}")
    print(f"  - 跳过(无匹配NP): {skipped_np}")
    print(f"  - 跳过(无匹配BR): {skipped_br}")
    print(f"  - 跳过(重复): {skipped_dup}")

    return records


def insert_to_db(conn, records, batch_size=5000):
    """批量插入数据库"""
    cur = conn.cursor()

    # 插入SQL
    insert_sql = """
        INSERT INTO bio_resource_natural_products (
            bio_resource_id, natural_product_id, content_part, ref_id, ref_id_type
        ) VALUES %s
        ON CONFLICT (bio_resource_id, natural_product_id) DO NOTHING
    """

    # 转换为元组列表
    values = [
        (r['bio_resource_id'], r['natural_product_id'], r['content_part'], r['ref_id'], r['ref_id_type'])
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
        if inserted % 100000 == 0 or inserted == total:
            print(f"  - 进度: {inserted}/{total} ({100*inserted/total:.1f}%)")

    # 验证
    cur.execute("SELECT COUNT(*) FROM bio_resource_natural_products")
    count = cur.fetchone()[0]
    print(f"[{datetime.now()}] 导入完成! 表中总记录数: {count}")

    cur.close()
    return count


def main():
    print("=" * 60)
    print("生物资源-天然产物关联数据导入脚本")
    print("=" * 60)

    # 连接数据库
    print(f"[{datetime.now()}] 连接数据库...")
    conn = psycopg2.connect(**DB_CONFIG)

    # 加载ID映射
    np_map, br_map = load_id_mappings(conn)

    # 处理NPASS数据
    npass_records, seen_pairs = process_npass_data(np_map, br_map)

    # 处理CMAUP数据
    cmaup_records = process_cmaup_data(np_map, br_map, seen_pairs)

    # 合并记录
    all_records = npass_records + cmaup_records
    print(f"[{datetime.now()}] 总关联记录数: {len(all_records)}")

    # 插入数据库
    count = insert_to_db(conn, all_records)

    conn.close()

    print("=" * 60)
    print(f"导入完成! 共导入 {count} 条关联记录")
    print("=" * 60)


if __name__ == '__main__':
    main()
